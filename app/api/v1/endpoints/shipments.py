from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.shipment import ShipmentUpdate, ShipmentOut
from app.services import shipment_service
from app.core.security import decode_token
from typing import List, Optional

router = APIRouter()

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    token = authorization.replace("Bearer ", "")
    try: return decode_token(token)
    except: raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/", response_model=List[ShipmentOut])
def all_shipments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.get("is_admin"): raise HTTPException(403, "Solo admin")
    return shipment_service.get_all(db)

@router.put("/{sid}")
def update(sid: int, data: ShipmentUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.get("is_admin"): raise HTTPException(403, "Solo admin")
    return shipment_service.update_shipment(db, sid, data)
