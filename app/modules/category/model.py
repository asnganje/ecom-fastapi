from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer)
    name:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id:Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

