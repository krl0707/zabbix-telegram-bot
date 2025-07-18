# Zabbix Telegram Bot (Secure & Refactored)

Улучшенная версия Telegram бота для интеграции с Zabbix с исправлением проблем безопасности и архитектуры.

## Основные функции
- Получение и обработка алертов из Zabbix
- Команды:
  - `/mute [hours]` - временное отключение уведомлений
  - `/graph [triggerid]` - графики исторических данных (в разработке)
  - `/history_tags` - история срабатываний по тегам (в разработке)

## Установка
```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/zabbix-telegram-bot.git
cd zabbix-telegram-bot

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать конфигурационный файл
cp config.example.json config.json

# 4. Заполнить конфигурацию (см. SETUP.md)
# 5. Запустить бота
python -m src.main