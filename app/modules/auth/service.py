from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password, create_access_token, verify_password
from app.modules.auth.schema import RegisterRequest, LoginRequest
from app.modules.users.repository import UserRepository
from app.modules.users.model import User
from app.modules.users.schemas import UserRole, UserRead


class AuthService():
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def _dump_user(self, user:User)->dict:
        return UserRead.model_validate(user).model_dump()

    def register(self, payload: RegisterRequest) -> dict:
        existing_user = self.user_repository.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        user = User(
            full_name = payload.full_name,
            email = payload.email,
            password_hash = hash_password(payload.password),
            is_active=True,
            role=UserRole.CUSTOMER.value
        )

        db_user = self.user_repository.create_user(user)
        created_user = self._dump_user(db_user)
        access_token = create_access_token(str(db_user.id), db_user.role)
        return {
                "access_token:":access_token,
                "user":created_user
                }
    def login(self, payload:LoginRequest)->dict:
        user = self.user_repository.get_user_by_email(payload.email)
        if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        access_token = create_access_token(str(user.id), user.role)
        pydantic_user = self._dump_user(user)
        return {
            "access_token:": access_token,
            "user": pydantic_user
        }








