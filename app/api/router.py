from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as user_router
from app.modules.category.router import router as category_router
from app.modules.product.router import router as product_router
from app.modules.cart.router import router as cart_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(category_router, prefix="/categories", tags=["Category"])
api_router.include_router(product_router, prefix="/products", tags=["Product"])
api_router.include_router(cart_router, prefix="/carts", tags=["Cart"])
