from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_all(db: Session): return db.query(Product).all()
def get_one(db: Session, pid: int): return db.query(Product).filter(Product.id == pid).first()

def create(db: Session, data: ProductCreate):
    p = Product(**data.dict())
    db.add(p); db.commit(); db.refresh(p); return p

def update(db: Session, pid: int, data: ProductUpdate):
    p = get_one(db, pid)
    if p:
        for k, v in data.dict().items(): setattr(p, k, v)
        db.commit(); db.refresh(p)
    return p

def delete(db: Session, pid: int):
    p = get_one(db, pid)
    if p: db.delete(p); db.commit()
    return p
