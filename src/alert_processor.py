import re
from loguru import logger
from src.models.alert import AlertData
from src.models.config import AppConfig
from src.commands.utils import send_telegram_message

def parse_alert_message(message: str) -> AlertData:
    """Парсинг сообщения от Zabbix с использованием регулярных выражений"""
    try:
        # Пример парсинга (реализация зависит от формата сообщения)
        host_match = re.search(r"Host:\s*(.+)", message)
        trigger_match = re.search(r"Trigger:\s*(.+)", message)
        trigger_id_match = re.search(r"Trigger ID:\s*(\d+)", message)
        host_id_match = re.search(r"Host ID:\s*(\d+)", message)
        
        tags = {}
        tag_matches = re.findall(r"Tag:\s*(\w+)=([\w-]+)", message)
        for key, value in tag_matches:
            tags[key] = value
        
        return AlertData(
            host=host_match.group(1) if host_match else "Unknown",
            trigger=trigger_match.group(1) if trigger_match else "Unknown",
            trigger_id=trigger_id_match.group(1) if trigger_id_match else None,
            host_id=host_id_match.group(1) if host_id_match else None,
            tags=tags,
            valid=bool(trigger_id_match and host_id_match)
        )
    except Exception as e:
        logger.error(f"Alert parsing error: {str(e)}")
        return AlertData(valid=False)

def process_alert(subject: str, message: str, config: AppConfig) -> None:
    """Обработка входящего алерта от Zabbix"""
    try:
        # Парсинг алерта
        alert_data = parse_alert_message(message)
        
        # Форматирование сообщения для Telegram
        alert_text = f"*{subject}*\n\n"
        alert_text += f"Host: {alert_data.host}\n"
        alert_text += f"Trigger: {alert_data.trigger}\n"
        
        if alert_data.trigger_id:
            alert_text += f"Trigger ID: `{alert_data.trigger_id}`\n"
        
        if alert_data.tags:
            tags_str = ", ".join([f"{k}={v}" for k, v in alert_data.tags.items()])
            alert_text += f"Tags: {tags_str}\n"
        
        alert_text += "\nКоманды:\n/mute - отключить уведомления"
        
        # Отправка сообщения
        send_telegram_message(config, alert_text)
        
    except Exception as e:
        logger.error(f"Alert processing failed: {str(e)}")