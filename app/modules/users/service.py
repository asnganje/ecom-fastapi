from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRead, UserUpdate, UserRole


class UserService():
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    def _dump_user(self, user:User)->dict:
        return UserRead.model_validate(user).model_dump()

    def list_users(self)->list[dict]:
        users = self.repository.get_all_users()
        results = [self._dump_user(user) for user in users]
        return results
    def get_user(self, user_id) -> dict:
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        result = self._dump_user(user)
        return result
    def get_current_user(self, user:User)->dict:
        return self._dump_user(user)

    def update_user(self, user_id:int, payload: UserUpdate) ->dict:
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        changes = payload.model_dump(exclude_unset=True, exclude_none=True)
        if "full_name" in changes.keys():
            user.full_name = changes["full_name"]
        db_user = self.repository.update_user(user)
        return self._dump_user(db_user)
    def delete_user(self, user_id:int)->None:
        db_user = self.repository.get_user_by_id(user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        self.repository.delete_user(db_user)
    def ensure_admin(self)->None:
        admin_email = "asn1@gmail.com"
        admin_password = "passwordsecret"

        existing_admin = self.repository.get_user_by_email(admin_email)
        if existing_admin is not None:
            return
        admin_user = User(
            full_name="nganje ozil",
            email=admin_email,
            password_hash=hash_password(admin_password),
            is_active=True,
            role=UserRole.ADMIN.value
        )

        self.repository.create_user(admin_user)







