from sqlalchemy import Integer, String, Float, Boolean, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from app.modules.category.model import Category


class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(150), nullable=False)
    brand_name:Mapped[str] = mapped_column(String(100), nullable=False)
    model_number:Mapped[str] = mapped_column(String(100), nullable=False)
    description:Mapped[str] = mapped_column(String(500), nullable=False)
    warranty:Mapped[str] = mapped_column(String(255), nullable=False)
    discount_percent:Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity:Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    highlights:Mapped[list[str]] = mapped_column(JSON, nullable=False)
    specifications:Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False)
    additional_images:Mapped[list[str]] = mapped_column(JSON, nullable=False)
    price:Mapped[float] = mapped_column(Float, nullable=False)
    image_url:Mapped[str] = mapped_column(String(255), nullable=False)
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category:Mapped["Category"] = relationship()

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

