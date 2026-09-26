from sqlalchemy.orm import Session;
from app.modules.users.model import User
from sqlalchemy import select

class UserRepository():
    def __init__(self, db:Session)->None:
        self.db = db
    def get_all_users(self)->list[User]:
        statement = select(User).order_by(User.id)
        return self.db.scalars(statement).all()
    def get_user_by_id(self, user_id:int)->User|None:
        return self.db.get(User, user_id)
    def get_user_by_email(self, email:str)->User|None:
        statement = select(User).where(User.email == email)
        return self.db.scalars(statement).one_or_none()
    def create_user(self, user:User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    def update_user(self, user:User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user
    def delete_user(self, user:User) -> None:
        self.db.delete(user)
        self.db.commit()





