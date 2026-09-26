from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
class User(Base):
    __table_names = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role:Mapped[str] = mapped_column(String(50), default="customer", nullable=False)


