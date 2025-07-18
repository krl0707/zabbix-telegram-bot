import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            trigger_id TEXT NOT NULL,
            host_id TEXT NOT NULL,
            tags TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            maintenance_id TEXT NOT NULL,
            trigger_id TEXT NOT NULL,
            host_id TEXT NOT NULL,
            mute_until DATETIME NOT NULL
        )''')
        self.conn.commit()
    
    def add_alert(self, chat_id, trigger_id, host_id, tags):
        self.conn.execute('''
        INSERT INTO alerts (chat_id, trigger_id, host_id, tags)
        VALUES (?, ?, ?, ?)
        ''', (chat_id, trigger_id, host_id, json.dumps(tags)))
        self.conn.commit()
    
    def get_last_alert(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT trigger_id, host_id, tags
        FROM alerts
        WHERE chat_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        ''', (chat_id,))
        result = cursor.fetchone()
        return (result[0], result[1], json.loads(result[2])) if result else (None, None, None)
    
    def add_mute(self, chat_id, maintenance_id, trigger_id, host_id, mute_until):
        self.conn.execute('''
        INSERT INTO mutes (chat_id, maintenance_id, trigger_id, host_id, mute_until)
        VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, maintenance_id, trigger_id, host_id, mute_until))
        self.conn.commit()
    
    def get_expired_mutes(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM mutes WHERE mute_until < datetime('now')
        ''')
        return cursor.fetchall()
    
    def delete_mute(self, mute_id):
        self.conn.execute('DELETE FROM mutes WHERE id = ?', (mute_id,))
        self.conn.commit()
        