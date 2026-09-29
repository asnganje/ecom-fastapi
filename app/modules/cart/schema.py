from pydantic import BaseModel, Field

class AddCartItemRequest(BaseModel):
    product_id:int = Field(gt=0)
    quantity:int = Field(default=1, gt=0)

class UpdateCartItemRequest(BaseModel):
    quantity:int = Field(gt=0)


class CartProductSummary:
    id:int
    name: str
    image_url: str
    discount_percent: float
    price: float
    selling_price:float


class CartItemRead(BaseModel):
    id:int
    product_id:int
    quantity:int
    unit_price:float
    unit_selling_price:float
    sub_total:float
    product: CartProductSummary

class CartRead(BaseModel):
    id:int|None
    user_id:int
    total_items:int
    total_amount:float
    items:list[CartItemRead]