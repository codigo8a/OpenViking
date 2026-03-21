import os
import markdown
import re

class SkillLoader:
    def __init__(self, skills_docs_path: str = "./skills/docs"):
        self.skills_docs_path = skills_docs_path

    def load_skill(self, skill_name: str):
        # Allow specifying extension or not
        if not skill_name.endswith(".md"):
            md_path = os.path.join(self.skills_docs_path, f"{skill_name}.md")
        else:
            md_path = os.path.join(self.skills_docs_path, skill_name)

        if not os.path.exists(md_path):
            raise FileNotFoundError(f"Skill {skill_name} not found in {self.skills_docs_path}.")
        
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return {
            "name": skill_name, 
            "content": content,
            "commands": self._extract_commands(content)
        }

    def list_skills(self):
        if not os.path.exists(self.skills_docs_path):
            return []
        return [f.replace(".md", "") for f in os.listdir(self.skills_docs_path) if f.endswith(".md")]

    def _extract_commands(self, content: str):
        # Basic regex to extract backticked commands from MD
        # This can be improved to be more specific to sections
        return re.findall(r"`([^`]+)`", content)
