from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(500))
    min_age = Column(Integer, default=0)
    max_age = Column(Integer, default=99)
    is_safe_certified = Column(Boolean, default=True)
    safety_notes = Column(String(300))
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
