from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderOut
from app.services import order_service
from app.core.security import decode_token
from typing import List, Optional

router = APIRouter()

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    token = authorization.replace("Bearer ", "")
    try: return decode_token(token)
    except: raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/", response_model=OrderOut)
def create_order(data: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return order_service.create_order(db, int(user["sub"]), data)

@router.get("/my")
def my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = order_service.get_user_orders(db, int(user["sub"]))
    result = []
    for o in orders:
        shipment_data = None
        if o.shipment:
            shipment_data = {
                "id": o.shipment.id,
                "address": o.shipment.address,
                "city": o.shipment.city,
                "status": o.shipment.status,
                "tracking_number": o.shipment.tracking_number,
            }
        result.append({
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "created_at": o.created_at,
            "shipment": shipment_data,
        })
    return result

@router.get("/")
def all_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.get("is_admin"): raise HTTPException(403, "Solo admin")
    orders = order_service.get_all_orders(db)
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "created_at": o.created_at,
        })
    return result

@router.put("/{oid}/status")
def update_status(oid: int, status: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.get("is_admin"): raise HTTPException(403, "Solo admin")
    return order_service.update_status(db, oid, status)

@router.delete("/{oid}")
def delete_order(oid: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.get("is_admin"): raise HTTPException(403, "Solo admin")
    return order_service.delete_order(db, oid)
