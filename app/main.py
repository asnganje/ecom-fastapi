from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine

app = FastAPI(
    title="E-commerce Project",
    description="A FastAPI backend API for an electronics ecommerce platform",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
def home():
    return {"message": "Welcome to electronics ecommerce API"}