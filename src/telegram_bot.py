from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackContext
)
from loguru import logger
from src.models.config import AppConfig
from src.commands import (
    mute_command,
    graph_command,
    history_tags_command
)

def run_bot(config: AppConfig):
    """Запуск Telegram бота"""
    application = Application.builder().token(config.telegram.bot_token).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("graph", graph_command))
    application.add_handler(CommandHandler("history_tags", history_tags_command))
    
    # Обработка ошибок
    application.add_error_handler(error_handler)
    
    logger.info("Starting Telegram bot...")
    application.run_polling()

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Обработка ошибок в боте"""
    logger.error(f"Bot error: {context.error}")
    
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Произошла ошибка при обработке команды"
        )