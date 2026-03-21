import json
from typing import List, Dict, Any, Optional
from llm.groq_client import GroqClient
from llm.openrouter_client import OpenRouterClient
from skills.loader import SkillLoader
from skills.executor import execute_command
from memory.sqlite_store import SQLiteStore

class AgentLoop:
    def __init__(self, groq: GroqClient, openrouter: OpenRouterClient, db: SQLiteStore, skills: SkillLoader, max_iters: int = 5):
        self.groq = groq
        self.openrouter = openrouter
        self.db = db
        self.skills = skills
        self.max_iters = max_iters

    def run(self, user_id: str, user_input: str):
        # 1. Load context
        history = self.db.get_chat_history(user_id)
        available_skills = self.skills.list_skills()
        
        system_prompt = f"""
Eres OpenViking, un agente de IA personal altamente capaz y seguro.
Tu objetivo es ayudar al usuario mediante el pensamiento lógico y la ejecución de herramientas.
Formato de respuesta obligatorio:
Pensamiento: <tu razonamiento interno de lo que vas a hacer>
Acción: <nombre_de_la_herramienta>(<parametros>) o "responder"
Observación: <resultado de la acción, lo rellenaré yo>

Herramientas disponibles:
- execute_shell_command(command: str): Ejecuta un comando en la consola Linux.
- get_skill_docs(skill_name: str): Obtiene la documentación de una habilidad para saber qué comandos usar.
- save_fact(key: str, value: str): Guarda información persistente.

Habilidades instaladas: {", ".join(available_skills)}

Sé conciso y directo. No inventes herramientas que no existan.
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append(msg)
        messages.append({"role": "user", "content": user_input})

        for i in range(self.max_iters):
            try:
                # Primary attempt with Groq
                response = self.groq.chat_completion(messages)
            except Exception as e:
                print(f"Groq failed: {e}. Falling back to OpenRouter.")
                response = self.openrouter.chat_completion(messages)

            print(f"Iteration {i+1}:\n{response}")
            
            # Simple parser for Action: tool(args)
            action_match = self._parse_action(response)
            
            if not action_match or action_match["tool"] == "responder":
                # Final response found in the thought or as a direct answer
                final_text = response.split("Pensamiento:")[-1].split("Acción:")[0].strip()
                if not final_text:
                    final_text = response
                return final_text

            # Execute tool
            tool = action_match["tool"]
            args = action_match["args"]
            
            observation = ""
            if tool == "execute_shell_command":
                observation = execute_command(args.get("command", ""))
            elif tool == "get_skill_docs":
                try:
                    skill_data = self.skills.load_skill(args.get("skill_name", ""))
                    observation = f"Documentación de {args.get('skill_name')}:\n{skill_data['content']}"
                except Exception as e:
                    observation = f"Error cargando skill: {e}"
            elif tool == "save_fact":
                self.db.save_memory(args.get("key", ""), args.get("value", ""))
                observation = "Hecho guardado correctamente."
            else:
                observation = f"Herramienta '{tool}' no reconocida."

            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "system", "content": f"Observación: {observation}"})
        
        return "He alcanzado el límite de iteraciones sin una respuesta definitiva."

    def _parse_action(self, text: str):
        # Very crude parser for Action: tool(args)
        if "Acción:" not in text:
            return None
        
        action_line = [line for line in text.split("\n") if "Acción:" in line][0]
        action_content = action_line.replace("Acción:", "").strip()
        
        if "(" not in action_content:
            return {"tool": action_content, "args": {}}
        
        import re
        match = re.search(r"(\w+)\((.*)\)", action_content)
        if match:
            tool = match.group(1)
            args_str = match.group(2)
            # Try to parse as JSON or simple key=value if possible, 
            # here we assume the agent provides valid-ish args or we just pass the raw string if single arg
            # For simplicity in this demo, we'll try to extract 'command' or 'skill_name'
            args = {}
            if tool == "execute_shell_command":
                # Extract content inside quotes if present
                cmd_match = re.search(r"command=['\"](.*?)['\"]", args_str)
                args["command"] = cmd_match.group(1) if cmd_match else args_str.strip("'\"")
            elif tool == "get_skill_docs":
                name_match = re.search(r"skill_name=['\"](.*?)['\"]", args_str)
                args["skill_name"] = name_match.group(1) if name_match else args_str.strip("'\"")
            elif tool == "save_fact":
                k_match = re.search(r"key=['\"](.*?)['\"]", args_str)
                v_match = re.search(r"value=['\"](.*?)['\"]", args_str)
                args["key"] = k_match.group(1) if k_match else "key"
                args["value"] = v_match.group(1) if v_match else "value"
            
            return {"tool": tool, "args": args}
        
        return {"tool": action_content, "args": {}}
