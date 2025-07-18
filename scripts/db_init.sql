CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    trigger_id TEXT NOT NULL,
    host_id TEXT NOT NULL,
    tags TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mutes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    maintenance_id TEXT NOT NULL,
    trigger_id TEXT NOT NULL,
    host_id TEXT NOT NULL,
    mute_until DATETIME NOT NULL
);

CREATE INDEX idx_mute_until ON mutes (mute_until);
CREATE INDEX idx_alerts_timestamp ON alerts (timestamp);
