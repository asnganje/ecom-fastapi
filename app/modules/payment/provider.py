from statistics import mode

import stripe
from fastapi import HTTPException, status

from app.core.config import settings


class StripeProvider:
    def __init__(self):
        stripe.api_key=settings.STRIPE_SECRET_KEY

    def create_payment_link(self, order_id:int, amount:float, user_email:str, user_name:str)->dict:
        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                customer_email=user_email,
                line_items=[
                    {
                        "price_data":{
                            "currency":"usd",
                            "product_data":{
                                "name":f"{order_id}",
                                "description":f"Payment for order #{order_id} by {user_name}"
                            },
                            "unit_amount":int(round(amount*100)),

                        },
                        "quantity":1
                    }
                ],
                success_url="http://localhost:8000/api/v1/payments/success",
                cancel_url="http://localhost:8000/api/v1/payments/failed",
                metadata={
                    "order_id":str(order_id)
                }
            )

            print(f"session..............{session}")

            return {
                "payment_link": session.url,
                "provider_payment_link_id":session.id,
            }
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc)
            ) from exc

    def get_payment_details(self, payment_id:str)->dict:
        try:
            session = stripe.checkout.Session.retrieve(payment_id)
            print(f"session.................{session}")
            return {
                "payment_id": session.id,
                "amount": session.amount_total,
                "status": session.payment_status,
                "is_paid": session.payment_status == "paid"
            }
        except Exception as exc:
            print(f"Error...................{exc}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="unable to fetch payment details"
            )

