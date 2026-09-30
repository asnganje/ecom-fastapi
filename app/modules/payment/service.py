from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.order.repository import OrderRepository
from app.modules.order.schema import OrderStatus, PaymentStatus
from app.modules.payment.model import Payment
from app.modules.payment.repository import PaymentRepository
from app.modules.payment.schema import CreatePaymentLinkRequest, PaymentLinkResponse, PaymentProvider
from app.modules.users.model import User
from app.modules.users.schemas import UserRole


class PaymentService:
    def __init__(self, db:Session):
        self.payment_repository = PaymentRepository(db)
        self.order_repository = OrderRepository(db)
    def _get_owned_order(self, order_id:int, current_user:User):
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Order not found!"
            )
        if current_user.role != UserRole.ADMIN.value and order.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied!"
            )
        return order

    def create_or_make_payment(self, current_user:User, payload:CreatePaymentLinkRequest)->PaymentLinkResponse:
        order = self._get_owned_order(payload.order_id, current_user)
        if order.status != OrderStatus.PENDING.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment link can only be created for pending orders"
            )
        if order.payment_status == PaymentStatus.PAID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order is already paid"
            )
        existing_payment = self.payment_repository.get_pending_payment_by_order_and_provider(
                                    order.id, payload.provider.value)
        if existing_payment is not None:
            return PaymentLinkResponse(
                order_id=order.id,
                provider=payload.provider,
                amount=existing_payment.amount,
                currency=existing_payment.currency,
                payment_link=existing_payment.payment_link_url,
                provider_payment_link_id=existing_payment.provider_payment_link_id
            )

        payment = Payment(
            order_id = order.id,
            user_id = current_user.id,
            provider=payload.provider,
            amount=order.total_amount,
            currency="USD",
            status=PaymentStatus.PENDING.value,
            payment_link_url="dummy link",
            provider_payment_link_id="dummy payment link id"
        )

        db_payment = self.payment_repository.create_payment(payment)
        return PaymentLinkResponse(
            order_id=order.id,
            provider=payload.provider,
            amount=db_payment.amount,
            currency=db_payment.currency,
            payment_link=db_payment.payment_link_url,
            provider_payment_link_id=db_payment.provider_payment_link_id
        )




