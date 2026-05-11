from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    address = Column(String(300), nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    tracking_number = Column(String(100))
    status = Column(String(50), default="preparing")
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    order = relationship("Order", back_populates="shipment")
