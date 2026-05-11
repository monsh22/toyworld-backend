from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemIn]
    address: str
    city: str
    state: str
    zip_code: str

class ShipmentInfo(BaseModel):
    id: int
    address: str
    city: Optional[str] = None
    status: str
    tracking_number: Optional[str] = None
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total: Optional[float] = None
    status: str
    created_at: datetime
    shipment: Optional[ShipmentInfo] = None
    class Config:
        from_attributes = True
