import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from agent.loop import AgentLoop
from bot.security import is_allowed

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Acceso denegado. No estás en la lista blanca.")
        return
    
    await update.message.reply_text("¡Hola! Soy OpenViking, tu agente de IA personal. ¿En qué puedo ayudarte hoy?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    if not is_allowed(user_id):
        # Already handled by start, but for safety in case they just text it
        return

    # Indicate the agent is thinking
    await update.message.chat.send_action(action="typing")
    
    # Get the agent loop from bot data (set up in main)
    agent = context.bot_data.get("agent_loop")
    if not agent:
        await update.message.reply_text("Error: Agente no inicializado.")
        return

    try:
        # Run the agent loop
        response = agent.run(str(user_id), user_text)
        
        # Save to history
        agent.db.add_chat_message(str(user_id), "user", user_text)
        agent.db.add_chat_message(str(user_id), "assistant", response)
        
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text(f"Ocurrió un error procesando tu solicitud: {str(e)}")
