from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShipmentUpdate(BaseModel):
    status: str
    tracking_number: Optional[str] = None

class ShipmentOut(BaseModel):
    id: int
    order_id: int
    address: str
    city: Optional[str] = None
    status: str
    tracking_number: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
