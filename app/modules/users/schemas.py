from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN="admin"
    CUSTOMER="customer"

class UserBase(BaseModel):
    full_name:str
    email:str

class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str | None
