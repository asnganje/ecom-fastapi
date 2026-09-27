from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.common.dependencies import get_db
from app.modules.users.schemas import UserUpdate, UserRole
from app.modules.users.service import UserService
from app.modules.users.model import User
from app.common.dependencies import get_current_user

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def list_users(current_user:User=Depends(get_current_user),
               db: Session=Depends(get_db)
               ) ->list[dict]:
    if current_user.role !=UserRole.ADMIN.value:
        raise HTTPException(
              status_code= status.HTTP_401_UNAUTHORIZED,
              detail="Only Admin can access this resource"
        )
    service=UserService(db)
    response = service.list_users()
    return response

@router.get("/profile", status_code=status.HTTP_200_OK)
def get_current_user_profile(
                             db: Session=Depends(get_db),
                             current_user: User = Depends(get_current_user))->dict:
    service = UserService(db)
    user = service.get_current_user(current_user)
    return user

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id:int, db: Session=Depends(get_db)):
    service = UserService(db)
    user = service.get_user(user_id)
    return user

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id:int, payload: UserUpdate, db: Session=Depends(get_db)):
    service = UserService(db)
    user = service.update_user(user_id, payload)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:int, current_user:User=Depends(get_current_user), db: Session= Depends(get_db)) -> dict:
    if current_user.role !=UserRole.ADMIN.value:
        raise HTTPException(
              status_code= status.HTTP_401_UNAUTHORIZED,
              detail="Only Admin can access this resource"
        )

    service = UserService(db)
    service.delete_user(user_id)
    return {"message":"User deleted successfully!"}



