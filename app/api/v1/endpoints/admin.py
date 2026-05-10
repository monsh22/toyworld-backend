from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import get_all_users, delete_user
from app.core.security import decode_token

router = APIRouter()

def get_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = decode_token(token)
        if not payload.get("is_admin"): raise HTTPException(403, "Solo admin")
        return payload
    except HTTPException: raise
    except: raise HTTPException(401, "Token inválido")

@router.get("/users")
def list_users(db: Session = Depends(get_db), admin=Depends(get_admin)):
    return get_all_users(db)

@router.delete("/users/{uid}")
def remove_user(uid: int, db: Session = Depends(get_db), admin=Depends(get_admin)):
    return delete_user(db, uid)
