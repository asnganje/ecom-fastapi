from fastapi import FastAPI
from app.database.session import SessionLocal
from app.api.router import api_router
from app.modules.users.model import User
from app.modules.product.model import Product
from app.modules.category.model import Category
from app.modules.cart.model import CartItem, Cart
from app.modules.order.model import OrderItem, Order
from app.modules.payment.model import Payment
from app.database.base import Base
from app.database.session import engine
from app.modules.users.service import UserService

app = FastAPI(
    title="E-commerce Project",
    description="A FastAPI backend API for an electronics ecommerce platform",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

db= SessionLocal()
try:
    UserService(db).ensure_admin()
finally:
    db.close()


@app.get("/", tags=["Root"])
def home():
    return {"message": "Welcome to electronics ecommerce API"}

app.include_router(api_router, prefix="/api/v1")