# OpenViking

OpenViking es un agente de IA personal diseñado para funcionar localmente en Linux y comunicarse exclusivamente a través de Telegram. Este agente utiliza un loop de razonamiento avanzado (Pensamiento -> Acción -> Observación) para ejecutar herramientas y habilidades de forma autónoma.

## Características

- 🤖 **Agente Inteligente**: Capacidad de razonamiento lógico utilizando LLMs (Groq / OpenRouter).
- 🛠️ **SkillHub**: Sistema de habilidades modular basado en archivos Markdown (`.md`).
- 🐚 **Ejecución de Comandos**: Capacidad para ejecutar comandos en la terminal de forma segura y autónoma.
- 🔒 **Seguridad**: Whitelist de IDs de usuario de Telegram y ejecución controlada.
- 🧠 **Memoria Persistente**: Almacenamiento de hechos e historial de chat con SQLite.

## Requisitos Previos

- Python 3.11 o superior.
- Una cuenta de Telegram y un bot creado vía [@BotFather](https://t.me/botfather).
- Una API Key de [Groq](https://console.groq.com/) (Principal) y/o [OpenRouter](https://openrouter.ai/) (Fallback).

## Instalación en Linux

Sigue estos pasos para configurar y ejecutar OpenViking en tu servidor o máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tuusuario/openviking
cd openviking
```

### 2. Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia el archivo `.env` de ejemplo y edítalo con tus credenciales:

```bash
cp .env .env.local  # O simplemente edita el .env existente
nano .env
```

Asegúrate de configurar:
- `TELEGRAM_BOT_TOKEN`: El token de tu bot.
- `TELEGRAM_ALLOWED_USER_IDS`: Tu ID de Telegram (puedes obtenerlo usando @userinfobot).
- `GROQ_API_KEY`: Tu clave de Groq.
- `DB_PATH`: Ruta a la base de datos (por defecto `./memory.db`).

### 5. Ejecutar el Agente
```bash
python3 main.py
```

## Uso del SkillHub

Para añadir una nueva habilidad, simplemente crea un archivo `.md` en la carpeta `skills/docs/`. El agente leerá la documentación para entender qué comandos debe ejecutar.

Ejemplo (`skills/docs/mi_error.md`):
```markdown
# Skill: Mi Error
Este skill permite limpiar los logs temporales.

## Comandos
`rm -rf /tmp/*.log`
```

## Estructura del Proyecto

- `agent/`: Lógica central del loop del agente.
- `bot/`: Manejadores de Telegram y seguridad.
- `llm/`: Clientes para Groq y OpenRouter.
- `memory/`: Persistencia con SQLite.
- `skills/`: Cargador de habilidades y ejecutor de comandos.
- `tools/`: Herramientas locales adicionales.
- `main.py`: Punto de entrada de la aplicación.
