import json
import logging
from datetime import datetime

def process_alert(subject, message, config, zabbix_api, db):
    """Обработка входящего алерта от Zabbix"""
    try:
        # Парсинг данных из алерта (реализация зависит от формата сообщения Zabbix)
        # Пример простой реализации:
        trigger_id = extract_value(message, "TRIGGER_ID")
        host_id = extract_value(message, "HOST_ID")
        tags = extract_tags(message)  # {"tag1": "value1", "tag2": "value2"}
        
        # Форматирование сообщения для Telegram
        formatted_msg = f"*{subject}*\n━━━━━━━━━━━━━━\n{message}\n"
        formatted_msg += f"Trigger ID: `{trigger_id}`\n"
        formatted_msg += "Команды:\n/graph - графики\n/history_tags - история\n/mute - отключить уведомления"
        
        # Отправка в Telegram
        send_telegram_message(config, formatted_msg)
        
        # Сохраняем алерт в БД для последующих команд
        db.add_alert(config['chat_id'], trigger_id, host_id, tags)
        
    except Exception as e:
        logging.error(f"Alert processing failed: {str(e)}")

def extract_value(message, key):
    """Извлечение значения из сообщения Zabbix"""
    # Реализация парсинга в зависимости от формата сообщения
    return "12345"  # Заглушка

def send_telegram_message(config, text):
    """Отправка сообщения через Telegram API"""
    import requests
    url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
    payload = {
        "chat_id": config['chat_id'],
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Telegram send error: {str(e)}")
        