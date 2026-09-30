from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user, get_db
from app.modules.order.schema import OrderRead, PlaceOrderRequest, OrderStatusUpdate
from app.modules.order.service import OrderService
from app.modules.users.model import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderRead)
def place_order(payload:PlaceOrderRequest, current_user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    o_service = OrderService(db)
    order=o_service.place_order(current_user, payload)
    return order

@router.get("/me", status_code=status.HTTP_200_OK, response_model=list[OrderRead])
def get_my_orders(current_user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    o_service = OrderService(db)
    return o_service.list_my_orders(current_user)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderRead])
def get_orders(current_user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    o_service = OrderService(db)
    return o_service.list_all_orders(current_user)

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderRead)
def get_order(order_id:int, current_user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    o_service = OrderService(db)
    return o_service.get_order(current_user, order_id)

@router.patch("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderRead)
def update_order_status(order_id:int, payload:OrderStatusUpdate, current_user:User=Depends(get_current_user), db: Session=Depends(get_db)):
    o_service = OrderService(db)
    return o_service.update_order_status(order_id, current_user, payload)



