from fastapi import APIRouter
from app.api.v1.endpoints import auth, products, orders, shipments, admin, chatbot, categories

api_router = APIRouter()
api_router.include_router(auth.router,       prefix="/auth",       tags=["Auth"])
api_router.include_router(products.router,   prefix="/products",   tags=["Products"])
api_router.include_router(orders.router,     prefix="/orders",     tags=["Orders"])
api_router.include_router(shipments.router,  prefix="/shipments",  tags=["Shipments"])
api_router.include_router(admin.router,      prefix="/admin",      tags=["Admin"])
api_router.include_router(chatbot.router,    prefix="/chatbot",    tags=["Chatbot"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
