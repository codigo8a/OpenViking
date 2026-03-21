# Skill: Google Workspace Integrator
Este skill permite al agente interactuar con Gmail, Drive y Docs de Google.

## Configuración Inicial
`pip install -r requirements.txt`

## Comandos Disponibles
Para listar archivos en Drive:
`python3 tools/google_cli.py list-drive`

Para listar correos electrónicos recibidos:
`python3 tools/google_cli.py list-gmail`

Para leer un documento de Google Docs:
`python3 tools/google_cli.py read-doc <document_id>`

## Requisitos
Asegúrate de que el archivo `service-account.json` esté en la raíz del proyecto y tenga los permisos adecuados para Drive y Gmail.
