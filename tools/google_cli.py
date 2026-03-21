import sys
import json
from tools.google_tools import GoogleWorkspaceManager

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m tools.google_cli <accion> [args...]")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    manager = GoogleWorkspaceManager()
    
    try:
        if action == "list-gmail":
            msgs = manager.list_gmail_messages()
            print(json.dumps(msgs, indent=2))
        elif action == "list-drive":
            files = manager.list_drive_files()
            print(json.dumps(files, indent=2))
        elif action == "read-doc":
            if len(sys.argv) < 3:
                print("Error: Document ID required.")
                return
            doc = manager.read_google_doc(sys.argv[2])
            print(doc)
        else:
            print(f"Acción '{action}' no reconocida.")
    except Exception as e:
        print(f"Error Google API: {str(e)}")

if __name__ == "__main__":
    main()
