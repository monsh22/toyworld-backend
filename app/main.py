from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.db.session import engine
from app.db import base  # noqa
from app.models import user, product, order, order_item, category, shipment  # noqa

# Importar modelos para que SQLAlchemy los registre
from app.db.base import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToyWorld API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "ToyWorld API 🧸"}
