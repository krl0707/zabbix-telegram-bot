# Инструкция по установке

## 1. Требования
- Python 3.10+
- Сервер Zabbix ≥ 5.0
- Аккаунт Telegram

## 2. Настройка Zabbix
1. Создайте API-пользователя с правами:
   - `read` для хостов, триггеров, элементов данных
   - `write` для периодов обслуживания

2. Настройте медиа-тип:
   - Имя: Telegram Bot
   - Тип: Скрипт
   - Параметры: `{ALERT.SUBJECT} {ALERT.MESSAGE}`

## 3. Установка бота
```bash
# Клонируйте репозиторий (после создания)
git clone https://github.com/ваш-аккаунт/zabbix-telegram-bot.git
cd zabbix-telegram-bot

# Установите зависимости
pip install -r requirements.txt

# Инициализируйте БД
sqlite3 zabbix_bot.db < scripts/db_init.sql

# Настройте конфигурацию
cp config.example.json config.json
nano config.json  # Заполните вашими данными
```
## 4. Запуск
```bash
# Тестовый режим (обработка алертов)
python src/zabbix_bot.py "Test Subject" "Test Message"

# Основной режим (бот)
python src/zabbix_bot.py
```
## 5. Настройка службы (systemd)
```bash

sudo nano /etc/systemd/system/zabbix-telegram-bot.service
```
Содержимое файла службы:
```ini

[Unit]
Description=Zabbix Telegram Bot
After=network.target

[Service]
User=zabbix
WorkingDirectory=/path/to/zabbix-telegram-bot
ExecStart=/usr/bin/python3 /path/to/zabbix-telegram-bot/src/zabbix_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Затем выполните:
```bash
sudo systemctl daemon-reload
sudo systemctl enable zabbix-telegram-bot
sudo systemctl start zabbix-telegram-bot
```