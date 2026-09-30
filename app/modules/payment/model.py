from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id:Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider:Mapped[str] = mapped_column(String(32), nullable=False)
    amount:Mapped[float] = mapped_column(Float, nullable=False)
    currency:Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    status:Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    payment_link_url:Mapped[str]=mapped_column(String(500), nullable=False)
    provider_payment_link_id:Mapped[str] = mapped_column(String(255), nullable=False)
    provider_payment_id:Mapped[str | None] = mapped_column(String(255), nullable=False)






