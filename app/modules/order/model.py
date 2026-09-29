from sqlalchemy import Integer, ForeignKey, Float, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.base import Base

class Order(Base):
    __tablename__ = "orders"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    total_items:Mapped[int] = mapped_column(Integer, nullable=False)
    total_amount:Mapped[float] = mapped_column(Float, nullable=False)
    status:Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    payment_status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                nullable=False,
                                                default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 default=func.now(),
                                                 onupdate=func.now()
                                                 )

class OrderItem(Base):
    __tablename__ = "order_items"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id:Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product_name:Mapped[str] = mapped_column(String(255), nullable=False)
    product_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    unit_selling_price: Mapped[float] = mapped_column(Float, nullable=False)
    sub_total: Mapped[float] = mapped_column(Float, nullable=False)






