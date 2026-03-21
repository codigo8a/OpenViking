import subprocess

def execute_command(command: str):
    """
    Executes a shell command and returns the stdout or stderr.
    """
    try:
        # Use shell=True to support pipes and aliases if needed, 
        # but be careful with unsanitized inputs.
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip() or "Comando ejecutado con éxito (sin salida)."
        else:
            return f"Error ejecutando comando: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Tiempo de ejecución excedido (timeout)."
    except Exception as e:
        return f"Excepción al ejecutar comando: {str(e)}"
