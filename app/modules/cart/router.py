from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user, get_db
from app.modules.cart.schema import CartRead, AddCartItemRequest, UpdateCartItemRequest
from app.modules.cart.service import CartService
from app.modules.users.model import User

router = APIRouter()

@router.get("/me", status_code=status.HTTP_200_OK, response_model=CartRead)
def get_my_cart(current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    c_service = CartService(db)
    return c_service.get_my_cart(current_user)

@router.post("/items", status_code=status.HTTP_201_CREATED, response_model=CartRead)
def add_item_to_cart(payload: AddCartItemRequest,
                     current_user:User = Depends(get_current_user),
                     db: Session=Depends(get_db)):
    c_service = CartService(db)
    return c_service.add_item(current_user, payload)

@router.patch("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartRead)
def update_cart_item(payload: UpdateCartItemRequest,
                     item_id:int,
                     current_user:User = Depends(get_current_user),
                     db: Session=Depends(get_db)):
    c_service = CartService(db)
    return c_service.update_item(current_user, item_id, payload)
@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartRead)
def remove_item(item_id:int, current_user:User = Depends(get_current_user),
                     db: Session=Depends(get_db)):
    c_service = CartService(db)
    return c_service.delete_item(current_user, item_id)

def clear_items(current_user:User = Depends(get_current_user),
                     db: Session=Depends(get_db)):
    c_service = CartService(db)
    return c_service.clear_cart(current_user)



