from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.modules.cart.model import Cart, CartItem


class CartRepository():
    def __init__(self, db: Session):
        self.db = db
    def get_active_cart_by_user_id(self, user_id) -> Cart | None:
        statement = select(Cart).where(Cart.user_id == user_id, Cart.is_active.is_(True))
        return self.db.scalar(statement).first()
    def create_cart(self, cart:Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart
    def get_items_by_cart_id(self, cart_id:int)->list[CartItem]|None:
        statement = select(CartItem).where(CartItem.cart_id == cart_id).order_by(CartItem.id.asc())

        return self.db.scalars(statement).all()

    def get_item_by_cart_and_product(self, cart_id:int, product_id:int )->CartItem|None:
        statement = select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id).order_by(CartItem.id.asc())
        return self.db.scalars(statement).first()

    def get_item_by_id(self, cart_item_id:int) -> CartItem | None:
        return self.db.get(CartItem, cart_item_id)

    def create_item(self, cart_item:CartItem)->CartItem:
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def update_cart_item(self, cart_item:CartItem)->CartItem:
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def delete_cart_item(self, cart_item:CartItem) -> None:
        self.db.delete(cart_item)
        self.db.commit()

    def clear_cart_items(self, cart_id:int)->None:
        statement = delete(CartItem).where(CartItem.cart_id == cart_id)
        self.db.commit()



