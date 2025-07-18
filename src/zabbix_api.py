import requests
import logging
from loguru import logger
from typing import List, Dict, Any
from src.models.config import AppConfig

class ZabbixAPIError(Exception):
    """Кастомное исключение для ошибок Zabbix API"""

class ZabbixAPI:
    def __init__(self, config: AppConfig):
        self.api_url = config.zabbix.api_url
        self.user = config.zabbix.user
        self.password = os.getenv("ZABBIX_PASSWORD")
        
        if not self.password:
            raise ValueError("ZABBIX_PASSWORD environment variable is not set")
        
        self.auth_token = self.authenticate()
        
    def authenticate(self) -> str:
        """Аутентификация в Zabbix API"""
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.password
            },
            "id": 1
        }
        
        response = self._request(payload)
        return response["result"]
    
    def _request(self, payload: Dict) -> Dict:
        """Базовый метод для запросов к API"""
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json-rpc"},
                timeout=10
            )
            response.raise_for_status()
            json_response = response.json()
            
            if "error" in json_response:
                error_msg = json_response["error"]["data"]
                logger.error(f"Zabbix API error: {error_msg}")
                raise ZabbixAPIError(error_msg)
                
            return json_response
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            raise ZabbixAPIError("Network error") from e
    
    def create_maintenance(self, host_ids: List[str], hours: int, tags: Dict[str, str]) -> str:
        """Создание периода обслуживания"""
        current_time = int(time.time())
        tag_list = [{"tag": k, "value": v} for k, v in tags.items()]
        
        payload = {
            "jsonrpc": "2.0",
            "method": "maintenance.create",
            "params": {
                "name": f"Telegram Mute: {tags}",
                "active_since": current_time,
                "active_till": current_time + hours * 3600,
                "hostids": host_ids,
                "tags": tag_list
            },
            "auth": self.auth_token,
            "id": 2
        }
        
        response = self._request(payload)
        return response["result"]["maintenanceids"][0]
    
    # Другие методы API...