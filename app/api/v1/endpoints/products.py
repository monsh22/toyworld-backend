from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import product_service
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return product_service.get_all(db)

@router.get("/{pid}", response_model=ProductOut)
def get_product(pid: int, db: Session = Depends(get_db)):
    return product_service.get_one(db, pid)

@router.post("/", response_model=ProductOut)
def create(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create(db, data)

@router.put("/{pid}", response_model=ProductOut)
def update(pid: int, data: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update(db, pid, data)

@router.delete("/{pid}")
def delete(pid: int, db: Session = Depends(get_db)):
    return product_service.delete(db, pid)
