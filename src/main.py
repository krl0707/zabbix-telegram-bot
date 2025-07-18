import sys
import os
import logging
from loguru import logger
from dotenv import load_dotenv
from src.models.config import AppConfig
from src.telegram_bot import run_bot
from src.alert_processor import process_alert

# Загрузка переменных окружения
load_dotenv()

def setup_logging(config: AppConfig):
    """Настройка системы логирования"""
    level = config.logging.level.upper()
    
    # Базовые настройки логирования
    logging.basicConfig(level=level)
    
    # Настройка Loguru
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    if config.logging.file_path:
        logger.add(
            config.logging.file_path,
            rotation="500 MB",
            retention="7 days",
            level=level
        )

def main():
    try:
        # Загрузка конфигурации
        config = AppConfig.load_from_file("config.json")
        
        # Настройка логирования
        setup_logging(config)
        
        # Режим обработки алертов
        if len(sys.argv) > 2:
            subject = sys.argv[1]
            message = sys.argv[2]
            process_alert(subject, message, config)
            return
        
        # Режим Telegram бота
        run_bot(config)
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()