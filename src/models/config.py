from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
import os

class TelegramConfig(BaseModel):
    bot_token: str = Field(..., min_length=10)
    chat_id: str = Field(..., min_length=5)

class ZabbixConfig(BaseModel):
    api_url: HttpUrl
    user: str

class MaintenanceConfig(BaseModel):
    group_id: int
    default_hours: int = 24

class LoggingConfig(BaseModel):
    level: str = "INFO"
    file_path: Optional[str] = None

class AppConfig(BaseModel):
    telegram: TelegramConfig
    zabbix: ZabbixConfig
    maintenance: MaintenanceConfig
    logging: LoggingConfig = LoggingConfig()

    @classmethod
    def load_from_file(cls, path: str) -> "AppConfig":
        with open(path, "r") as f:
            config_data = json.load(f)
        return cls(**config_data)