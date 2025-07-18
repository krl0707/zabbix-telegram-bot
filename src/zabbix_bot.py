#!/usr/bin/env python3
import sys
import json
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from zabbix_api import ZabbixAPI
from database import Database
from alert_processor import process_alert

# Загрузка конфигурации
with open('config.json') as f:
    config = json.load(f)

# Настройка логирования
logging.basicConfig(
    filename=config['log_path'],
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация компонентов
db = Database(config['db_path'])
zabbix = ZabbixAPI(
    config['zabbix_api_url'],
    config['zabbix_api_user'],
    config['zabbix_api_password'],
    config['zabbix_maintenance_groupid']
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Zabbix Bot активен! Используйте /help для списка команд")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📋 Доступные команды:
/graph [triggerid] - Графики данных за 24 часа
/history_tags - История срабатываний по тегам
/mute [часы] - Отключить уведомления (по умолч. 24ч)
/unmute - Включить уведомления
/mute_status - Активные отключения
"""
    await update.message.reply_text(help_text)

async def graph_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        trigger_id = context.args[0] if context.args else db.get_last_trigger(update.message.chat_id)
        if not trigger_id:
            await update.message.reply_text("❌ Trigger ID не указан и не найден в истории")
            return
        
        # Получаем данные и строим график
        items = zabbix.get_trigger_items(trigger_id)
        for item in items:
            history = zabbix.get_item_history(item['itemid'], config['graph_hours'])
            if history:
                plot_path = f"graph_{item['itemid']}.png"
                # Здесь должен быть код построения графика с помощью matplotlib
                await update.message.reply_photo(photo=open(plot_path, 'rb'))
    
    except Exception as e:
        logger.error(f"Graph command error: {str(e)}")
        await update.message.reply_text("⚠️ Ошибка при построении графиков")

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hours = int(context.args[0]) if context.args else config['default_mute_hours']
        chat_id = update.message.chat_id
        
        # Получаем последний триггер для этого чата
        trigger_id, host_id, tags = db.get_last_alert(chat_id)
        if not trigger_id:
            await update.message.reply_text("❌ Не найдено последних алертов для этого чата")
            return
        
        # Создаем maintenance в Zabbix
        maintenance_id = zabbix.create_maintenance([host_id], tags, hours)
        if maintenance_id:
            mute_until = datetime.now() + timedelta(hours=hours)
            db.add_mute(chat_id, maintenance_id, trigger_id, host_id, mute_until)
            await update.message.reply_text(f"🔇 Уведомления отключены на {hours} часов")
        else:
            await update.message.reply_text("❌ Ошибка при создании периода обслуживания")
    
    except Exception as e:
        logger.error(f"Mute command error: {str(e)}")
        await update.message.reply_text("⚠️ Ошибка при отключении уведомлений")

# Остальные команды (history_tags, unmute, mute_status) реализуются аналогично

def main():
    # Режим обработки алертов
    if len(sys.argv) > 2:
        process_alert(sys.argv[1], sys.argv[2], config, zabbix, db)
        return
    
    # Режим Telegram бота
    application = Application.builder().token(config['bot_token']).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("graph", graph_command))
    application.add_handler(CommandHandler("mute", mute_command))
    # Добавьте другие обработчики здесь
    
    # Настройка периодических задач
    job_queue = application.job_queue
    job_queue.run_repeating(auto_unmute, interval=3600, first=10)
    
    application.run_polling()

if __name__ == "__main__":
    main()
    