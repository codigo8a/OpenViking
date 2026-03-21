import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from memory.sqlite_store import SQLiteStore
from llm.groq_client import GroqClient
from llm.openrouter_client import OpenRouterClient
from agent.loop import AgentLoop
from skills.loader import SkillLoader
from bot.handlers import start, handle_message

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # 1. Initialize components
    db_path = os.getenv("DB_PATH", "./memory.db")
    db = SQLiteStore(db_path)
    
    groq_key = os.getenv("GROQ_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not groq_key:
        print("WARNING: GROQ_API_KEY not found in .env")
    
    groq = GroqClient(groq_key)
    openrouter = OpenRouterClient(openrouter_key)
    skills = SkillLoader(os.getenv("SKILLHUB_PATH", "./skills/docs"))
    
    agent = AgentLoop(groq, openrouter, db, skills)
    
    # 2. Setup Telegram Bot
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("CRITICAL: TELEGRAM_BOT_TOKEN not found in .env. Exiting.")
        return

    application = ApplicationBuilder().token(token).build()
    
    # Inject agent into bot data for access in handlers
    application.bot_data["agent_loop"] = agent

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("OpenViking is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
