from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.common.dependencies import get_db, get_current_user
from app.modules.category.schema import CategoryRead, CategoryCreate, CategoryUpdate
from app.modules.category.service import CategoryService
from app.modules.users.model import User
from app.modules.users.schemas import UserRole

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def list_categories(db:Session = Depends(get_db)) -> list[CategoryRead]:
    service = CategoryService(db)
    response = service.list_categories()
    return response

@router.get("/{category_id}", status_code=status.HTTP_200_OK)
def get_category(category_id:int, db:Session = Depends(get_db)) -> CategoryRead:
    service = CategoryService(db)
    category = service.get_category(category_id)
    return category

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate,
                    current_user: User = Depends(get_current_user),
                    db:Session = Depends(get_db)
                    ) -> CategoryRead:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to create a product category!"
        )
    service = CategoryService(db)
    category = service.create_category(payload)
    return category

@router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id:int,
                    payload: CategoryUpdate,
                    current_user: User = Depends(get_current_user),
                    db:Session = Depends(get_db)
                    ) -> CategoryRead:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to create a product category!"
        )
    service = CategoryService(db)
    updated_category = service.update_category(category_id, payload)
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
        category_id:int,
        current_user: User = Depends(get_current_user),
        db:Session = Depends(get_db)
        ) -> None:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin are allowed to create a product category!"
        )
    service = CategoryService(db)
    service.delete_category(category_id)

