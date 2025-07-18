
import requests
import json
import time
import logging

class ZabbixAPI:
    def __init__(self, url, user, password, maintenance_groupid):
        self.url = url
        self.maintenance_groupid = maintenance_groupid
        self.auth_token = self.authenticate(user, password)
        
    def authenticate(self, user, password):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {"user": user, "password": password},
            "id": 1
        }
        response = self._request(payload)
        return response['result'] if response and 'result' in response else None
    
    def _request(self, payload):
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers={'Content-Type': 'application/json-rpc'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Zabbix API error: {str(e)}")
            return None
    
    def get_trigger_items(self, triggerid):
        payload = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "triggerids": triggerid,
                "selectItems": "extend"
            },
            "auth": self.auth_token,
            "id": 2
        }
        response = self._request(payload)
        return response['result'][0]['items'] if response and 'result' in response else []
    
    def create_maintenance(self, hostids, tags, hours):
        current_time = int(time.time())
        tag_list = [{"tag": k, "value": v} for k, v in tags.items()]
        
        payload = {
            "jsonrpc": "2.0",
            "method": "maintenance.create",
            "params": {
                "name": f"Telegram Mute: {tags}",
                "active_since": current_time,
                "active_till": current_time + hours * 3600,
                "groups": [{"groupid": self.maintenance_groupid}],
                "timeperiods": [{"timeperiod_type": 0, "period": hours * 3600}],
                "tags": tag_list,
                "hostids": hostids
            },
            "auth": self.auth_token,
            "id": 3
        }
        response = self._request(payload)
        return response['result']['maintenanceids'][0] if response and 'result' in response else None
    
    def delete_maintenance(self, maintenance_id):
        payload = {
            "jsonrpc": "2.0",
            "method": "maintenance.delete",
            "params": [maintenance_id],
            "auth": self.auth_token,
            "id": 4
        }
        return self._request(payload)
    