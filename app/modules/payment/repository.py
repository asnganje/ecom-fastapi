from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.order.schema import PaymentStatus
from app.modules.payment.model import Payment


class PaymentRepository:
    def __init__(self, db:Session)->None:
        self.db = db

    def create_payment(self, payment:Payment)->Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update_payment(self, payment:Payment)->Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_pending_payment_by_order_and_provider(self, order_id:int, provider:str)->Payment | None:
        statement = select(Payment).where(
            Payment.order_id == order_id,
                        Payment.provider == provider,
                        Payment.status == PaymentStatus.PENDING.value
                )
        return self.db.scalars(statement).first()

    def get_by_order_and_provider(self, order_id:int, provider:str)->Payment | None:
        statement = select(Payment).where(
            Payment.order_id == order_id,
            Payment.provider == provider
        ).order_by(Payment.id.desc())

        return self.db.scalars(statement).first()




