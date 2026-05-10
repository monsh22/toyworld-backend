from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.core.security import decode_token
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

def get_admin(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    try:
        payload = decode_token(authorization.replace("Bearer ", ""))
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Solo admin")
        return payload
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), admin=Depends(get_admin)):
    cat = Category(name=data.name, description=data.description)
    db.add(cat); db.commit(); db.refresh(cat)
    return cat

@router.delete("/{cid}")
def delete_category(cid: int, db: Session = Depends(get_db), admin=Depends(get_admin)):
    cat = db.query(Category).filter(Category.id == cid).first()
    if cat: db.delete(cat); db.commit()
    return {"ok": True}
