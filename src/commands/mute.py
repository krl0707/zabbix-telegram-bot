from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from src.models.config import AppConfig
from src.zabbix_api import ZabbixAPI, ZabbixAPIError

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /mute"""
    try:
        # Получение конфигурации из контекста
        config: AppConfig = context.bot_data["config"]
        
        # Проверка ответа на сообщение
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Команда должна быть вызвана в ответ на сообщение с алертом")
            return
        
        # Парсинг аргументов
        hours = config.maintenance.default_hours
        if context.args and context.args[0].isdigit():
            hours = int(context.args[0])
        
        # Извлечение данных из алерта
        alert_text = update.message.reply_to_message.text
        alert_data = parse_alert_message(alert_text)
        
        if not alert_data.valid:
            await update.message.reply_text("❌ Не удалось извлечь данные алерта")
            return
        
        # Создание периода обслуживания
        zabbix_api = ZabbixAPI(config)
        maintenance_id = zabbix_api.create_maintenance(
            host_ids=[alert_data.host_id],
            hours=hours,
            tags=alert_data.tags
        )
        
        await update.message.reply_text(f"🔇 Уведомления отключены на {hours} часов")
        
    except ZabbixAPIError as e:
        logger.error(f"Zabbix API error: {str(e)}")
        await update.message.reply_text("❌ Ошибка при взаимодействии с Zabbix API")
    except Exception as e:
        logger.error(f"Mute command error: {str(e)}")
        await update.message.reply_text("⚠️ Произошла внутренняя ошибка")