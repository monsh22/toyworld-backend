from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.shipment import Shipment
from app.models.user import User
from app.schemas.order import OrderCreate
from app.services.notification_service import send_order_confirmation, send_admin_alert

def create_order(db: Session, user_id: int, data: OrderCreate):
    total = 0
    order = Order(user_id=user_id, status="pending")
    db.add(order); db.commit(); db.refresh(order)

    items_added = []
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock >= item.quantity:
            oi = OrderItem(order_id=order.id, product_id=item.product_id,
                           quantity=item.quantity, unit_price=product.price)
            # ✅ Automatización: reducir stock automáticamente
            product.stock -= item.quantity
            total += product.price * item.quantity
            items_added.append({"name": product.name, "qty": item.quantity})
            db.add(oi)

    order.total = total
    shipment = Shipment(order_id=order.id, address=data.address,
                        city=data.city, state=data.state, zip_code=data.zip_code)
    db.add(shipment); db.commit(); db.refresh(order)

    # ✅ Automatización: notificaciones
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        send_order_confirmation(order.id, user.name, user.email, total, items_added)
        send_admin_alert(order.id, user.name, total, len(items_added))

    return order

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_all_orders(db: Session):
    return db.query(Order).all()

def update_status(db: Session, order_id: int, status: str):
    o = db.query(Order).filter(Order.id == order_id).first()
    if o: o.status = status; db.commit(); db.refresh(o)
    return o

def delete_order(db: Session, order_id: int):
    o = db.query(Order).filter(Order.id == order_id).first()
    if o: db.delete(o); db.commit()
    return o
