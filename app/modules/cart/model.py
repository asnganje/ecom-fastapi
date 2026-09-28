from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Cart(Base):
    __tablename__ = "carts"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class CartItem(Base):
    __tablename__ = "cart_items"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id:Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity:Mapped[int] = mapped_column(Integer, nullable=False, default=1)