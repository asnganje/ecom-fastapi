from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.price import calculate_selling_price
from app.modules.cart.model import Cart, CartItem
from app.modules.cart.schema import CartRead, CartItemRead, CartProductSummary, AddCartItemRequest, \
    UpdateCartItemRequest
from app.modules.users.model import User
from app.modules.cart.repository import CartRepository
from app.modules.product.repository import ProductRepository


class CartService:
    def __init__(self, db:Session)->None:
        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)
    def _build_cart_response(self, user_id:int, cart: Cart | None):
        if cart is None:
            return CartRead(
                id = None,
                user_id = user_id,
                total_items = 0,
                total_amount = 0.0,
                items = []
            )
        cart_items = self.cart_repository.get_items_by_cart_id(cart.id)

        serialized_items: list[CartItemRead] = []
        total_items = 0
        total_amount = 0.0

        for item in cart_items:
            product = self.product_repository.get_product_by_id(item.product_id)
            if product is None:
                continue
            selling_price = calculate_selling_price(product.price, product.discount_percent)
            sub_total = round(selling_price * item.quantity, 2)
            cart_item_read = CartItemRead(
                id = item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
                unit_selling_price=selling_price,
                sub_total=sub_total,
                product=CartProductSummary(
                    id=product.id,
                    name=product.name,
                    image_url=product.image_url,
                    discount_percent=product.discount_percent,
                    price=product.price,
                    selling_price=selling_price
                )
            )
            serialized_items.append(cart_item_read)
            total_items+=item.quantity
            total_amount+=sub_total
        return CartRead(
           id=cart.id,
           user_id=user_id,
           total_items=total_items,
           total_amount=total_amount,
           items=serialized_items
        )

    def _get_or_create_active_cart(self, user_id:int) -> Cart:
        cart = self.cart_repository.get_active_cart_by_user_id(user_id)

        if cart is not None:
            return cart
        return self.cart_repository.create_cart(Cart(user_id=user_id, is_active=True))

    def _validate_product_for_cart(self, product_id:int):
        product = self.product_repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product does not exist"
            )
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product is inactive or expired"
            )
        return product

    def get_my_cart(self, current_user:User) ->CartRead:
        cart = self.cart_repository.get_active_cart_by_user_id(current_user.id)
        user_id = current_user.id
        cart_read = self._build_cart_response(user_id, cart)
        return cart_read
    def add_item(self, current_user:User, payload:AddCartItemRequest) ->CartRead:
        product_id = payload.product_id
        user_id = current_user.id
        product = self._validate_product_for_cart(product_id)
        cart = self._get_or_create_active_cart(user_id)

        existing_item = self.cart_repository.get_item_by_cart_and_product(cart.id, product.id)
        new_quantity = payload.quantity

        if existing_item is not None:
            new_quantity += existing_item.quantity
        if new_quantity > product.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock not available"
            )
        # to confirm
        if existing_item is not None:
            existing_item.quantity = new_quantity
            self.cart_repository.update_cart_item(existing_item)
        else:
            self.cart_repository.create_item(CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=payload.quantity
            ))
        return self._build_cart_response(user_id, cart)

    def update_item(self, current_user: User, item_id:int, payload:UpdateCartItemRequest)->CartRead:
        user_id = current_user.id
        cart = self.cart_repository.get_active_cart_by_user_id(user_id)
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        item = self.cart_repository.get_item_by_id(item_id)
        if item is None or item.cart_id != cart.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        product = self._validate_product_for_cart(item.product_id)

        if payload.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock not available"
            )
        item.quantity += payload.quantity
        self.cart_repository.update_cart_item(item)
        return self._build_cart_response(user_id, cart)

    def delete_item(self, current_user:User, item_id:int)->CartRead:
        user_id = current_user.id
        cart = self.cart_repository.get_active_cart_by_user_id(user_id)
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )

        item = self.cart_repository.get_item_by_id(item_id)
        if item is None or item.cart_id != cart.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        self.cart_repository.delete_cart_item(item)
        return self._build_cart_response(user_id, cart)

    def clear_cart(self, current_user:User)->CartRead:
        user_id = current_user.id
        cart = self.cart_repository.get_active_cart_by_user_id(user_id)
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        self.cart_repository.clear_cart_items(cart.id)
        return self._build_cart_response(user_id, cart)












