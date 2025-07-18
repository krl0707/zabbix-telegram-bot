from typing import Dict, Optional
from pydantic import BaseModel

class AlertData(BaseModel):
    """Модель данных алерта"""
    host: str
    trigger: str
    trigger_id: Optional[str] = None
    host_id: Optional[str] = None
    tags: Dict[str, str] = {}
    valid: bool = True