from fastapi import FastAPI

app = FastAPI(
    title="E-commerce Project",
    description="A FastAPI backend API for an electronics ecommerce platform",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def home():
    return {"message": "Welcome to electronics ecommerce API"}