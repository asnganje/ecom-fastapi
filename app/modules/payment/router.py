from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user, get_db
from app.modules.payment.schema import CreatePaymentLinkRequest, PaymentLinkResponse, VerifyPaymentRequest
from app.modules.payment.service import PaymentService
from app.modules.users.model import User

router = APIRouter()


@router.post("/create-link", status_code=status.HTTP_201_CREATED, response_model=PaymentLinkResponse)
def create_payment(
        payload:CreatePaymentLinkRequest,
        current_user:User=Depends(get_current_user),
        db:Session=Depends(get_db)
        ):
    p_service = PaymentService(db)
    return p_service.create_or_make_payment(current_user, payload)

@router.post("/verify", status_code=status.HTTP_200_OK, response_model=dict)
def verify_payment(payload: VerifyPaymentRequest, current_user:User=Depends(get_current_user),
        db:Session=Depends(get_db)):
    p_service = PaymentService(db)
    return p_service.verify_payment(current_user, payload)

