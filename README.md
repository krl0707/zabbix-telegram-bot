# Zabbix Telegram Bot

Расширенный Telegram-бот для интеграции с Zabbix, предоставляющий:
- Получение и обработка алертов
- Построение графиков исторических данных
- Анализ истории срабатываний триггеров
- Управление уведомлениями (временное отключение)

## Основные команды
- `/graph [triggerid]` - графики данных за 24 часа
- `/history_tags` - история срабатываний с теми же тегами
- `/mute [hours]` - отключить уведомления (по умолчанию 24 часа)
- `/unmute` - включить уведомления досрочно
- `/mute_status` - показать активные отключения

## Установка
```bash
pip install -r requirements.txt
sqlite3 zabbix_bot.db < scripts/db_init.sql
# Заполните config.json на основе config.example.json
python src/zabbix_bot.py
```