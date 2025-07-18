import pytest
from unittest.mock import patch, MagicMock
from src.zabbix_api import ZabbixAPI, ZabbixAPIError
from src.models.config import AppConfig, ZabbixConfig

@pytest.fixture
def mock_config():
    return AppConfig(
        telegram=TelegramConfig(bot_token="test", chat_id="test"),
        zabbix=ZabbixConfig(api_url="http://test.zabbix/api", user="test"),
        maintenance=MaintenanceConfig(group_id=15)
    )

@patch('requests.post')
def test_zabbix_api_authentication_success(mock_post, mock_config):
    # Подготовка мок-ответа
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "auth_token", "error": None}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    # Тестирование
    with patch.dict('os.environ', {'ZABBIX_PASSWORD': 'test_pass'}):
        api = ZabbixAPI(mock_config)
        assert api.auth_token == "auth_token"

@patch('requests.post')
def test_zabbix_api_authentication_failure(mock_post, mock_config):
    # Подготовка мок-ошибки
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": {"data": "Invalid credentials"}}
    mock_post.return_value = mock_response
    
    # Тестирование и проверка исключения
    with patch.dict('os.environ', {'ZABBIX_PASSWORD': 'test_pass'}):
        with pytest.raises(ZabbixAPIError):
            ZabbixAPI(mock_config)