from fastapi import FastAPI

from app.api.router import api_router
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.modules.users.service import UserService

app = FastAPI(
    title="E-commerce Project",
    description="A FastAPI backend API for an electronics ecommerce platform",
    version="1.0.0"
)

db= SessionLocal()
UserService(db).ensure_admin()

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
def home():
    return {"message": "Welcome to electronics ecommerce API"}

app.include_router(api_router, prefix="/api/v1")