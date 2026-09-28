
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, get_current_user
from app.modules.product.schema import ProductRead, ProductCreate, ProductUpdate
from app.modules.product.service import ProductService
from app.modules.users.model import User
from app.modules.users.schemas import UserRole

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_products(
        page:int = Query(default=1, ge=1),
        limit:int = Query(default=10, ge=1, le=100),
        db: Session=Depends(get_db)
        ) -> dict:
    service = ProductService(db)
    response = service.get_all_products(page, limit)
    return response

@router.get("/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id:int, db: Session=Depends(get_db)) -> ProductRead:
    service = ProductService(db)
    response = service.get_product(product_id)
    return response
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
        payload:ProductCreate,
        current_user: User = Depends(get_current_user),
        db: Session=Depends(get_db)) -> ProductRead:

    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to access this resource!"
        )

    service = ProductService(db)
    product = service.create_product(payload)
    return product
@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(
        product_id:int,
        payload:ProductUpdate,
        current_user: User = Depends(get_current_user),
        db: Session=Depends(get_db)) -> ProductRead:

    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to access this resource!"
        )

    service = ProductService(db)
    updated_product = service.update_product(product_id, payload)
    return updated_product
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id:int,
                   current_user: User = Depends(get_current_user),
                   db: Session=Depends(get_db)) -> None:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to access this resource!"
        )
    service= ProductService(db)
    service.delete_product(product_id)