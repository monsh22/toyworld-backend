from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None
    min_age: int = 0
    max_age: int = 99
    is_safe_certified: bool = True
    safety_notes: Optional[str] = None
    category_id: Optional[int] = None

class ProductUpdate(ProductCreate):
    pass

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True
