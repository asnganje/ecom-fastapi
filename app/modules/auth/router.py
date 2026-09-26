from fastapi import APIRouter, Depends, status

from app.common.dependencies import get_db
from app.modules.auth.schema import RegisterRequest, LoginRequest
from sqlalchemy.orm import Session

from app.modules.auth.service import AuthService

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db))->dict:
    service = AuthService(db)
    response = service.register(payload)
    return response

@router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
def login(payload: LoginRequest, db: Session = Depends(get_db))->dict:
    service = AuthService(db)
    response = service.login(payload)
    return response