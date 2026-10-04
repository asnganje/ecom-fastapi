from pydantic import BaseModel
from enum import Enum

from app.modules.order.schema import PaymentStatus, OrderStatus


class PaymentProvider(str, Enum):
    STRIPE = "STRIPE"


class CreatePaymentLinkRequest(BaseModel):
    order_id:int
    provider:PaymentProvider

class VerifyPaymentRequest(BaseModel):
    order_id:int
    provider:PaymentProvider
    payment_id:str


class PaymentLinkResponse(BaseModel):
    order_id:int
    provider: PaymentProvider
    amount:float
    currency:str
    payment_link:str
    provider_payment_link_id:str

class PaymentVerifyResponse(BaseModel):
    order_id:int
    payment_status:PaymentStatus
    order_status:OrderStatus
    provider:PaymentProvider
    payment_id:str
