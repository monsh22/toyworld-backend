from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.models.order import Order
from app.models.user import User
from app.schemas.shipment import ShipmentUpdate
from app.services.notification_service import send_shipment_update

def get_all(db: Session): return db.query(Shipment).all()

def get_by_order(db: Session, order_id: int):
    return db.query(Shipment).filter(Shipment.order_id == order_id).first()

def update_shipment(db: Session, shipment_id: int, data: ShipmentUpdate):
    s = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if s:
        s.status = data.status
        if data.tracking_number:
            s.tracking_number = data.tracking_number
        db.commit(); db.refresh(s)

        # ✅ Automatización: notificar al cliente del cambio
        order = db.query(Order).filter(Order.id == s.order_id).first()
        if order:
            user = db.query(User).filter(User.id == order.user_id).first()
            if user:
                send_shipment_update(order.id, user.name, user.email, data.status, data.tracking_number)
    return s
