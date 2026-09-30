from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.common.price import calculate_selling_price
from app.modules.address.repository import AddressRepository
from app.modules.cart.repository import CartRepository
from app.modules.order.model import Order, OrderItem
from app.modules.order.repository import OrderRepository
from app.modules.order.schema import OrderRead, PlaceOrderRequest, OrderStatus, PaymentStatus, OrderStatusUpdate
from app.modules.product.repository import ProductRepository
from app.modules.users.model import User
from app.modules.users.schemas import UserRole


class OrderService():
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)
        self.address_repository = AddressRepository(db)
        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    def _dump_order(self, order:Order)->OrderRead:
        items=self.order_repository.get_order_items_by_order_id(order.id)
        order_read= OrderRead(
            id=order.id,
            user_id=order.user_id,
            shipping_address_id=order.shipping_address_id,
            total_items=order.total_items,
            total_amount=order.total_amount,
            status=order.status,
            payment_status=order.payment_status,
            items=items
        )
        return order_read

    def place_order(self, current_user:User, payload:PlaceOrderRequest)->OrderRead:
        shipping_address = self.address_repository.get_address_by_id(payload.shipping_address_id)

        if shipping_address is None or shipping_address.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipping address not found"
            )
        cart = self.cart_repository.get_active_cart_by_user_id(current_user.id)
        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shopping cart not found"
            )

        cart_items = self.cart_repository.get_items_by_cart_id(cart.id)

        order_items:list[OrderItem] =[]
        total_items = 0
        total_amount=0

        for cart_item in cart_items:
            product = self.product_repository.get_product_by_id(cart_item.product_id)

            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not active"
                )
            if cart_item.quantity > product.stock_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient stock"
                )
            unit_selling_price = calculate_selling_price(product.price, product.discount_percent)
            sub_total = unit_selling_price*cart_item.quantity
            total_amount += sub_total
            total_items += cart_item.quantity
            product.stock_quantity -= cart_item.quantity

            order_item = OrderItem(
                order_id=0,
                product_id=product.id,
                product_name=product.name,
                quantity=cart_item.quantity,
                product_img_url=product.image_url,
                unit_price=product.price,
                unit_selling_price=unit_selling_price,
                sub_total=sub_total
            )

            order_items.append(order_item)

        order = Order(
            user_id=current_user.id,
            shipping_address_id = shipping_address.id,
            total_amount=total_amount,
            total_items=total_items,
            status=OrderStatus.PENDING.value,
            payment_status=PaymentStatus.PENDING.value
        )

        db_order = self.order_repository.place_order(order, order_items, cart_items)

        return self._dump_order(db_order)


    def list_my_orders(self, current_user:User)->list[OrderRead]:
        orders = self.order_repository.get_order_by_user_id(current_user.id)
        return [self._dump_order(order) for order in orders]

    def list_all_orders(self, current_user:User)->list[OrderRead]:
        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied"
            )
        orders = self.order_repository.get_all_orders()
        return [self._dump_order(order) for order in orders]
    def get_order(self, current_user:User, order_id:int)->OrderRead:
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        if current_user.role != UserRole.ADMIN.value and order.user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied"
            )
        return self._dump_order(order)
    def update_order_status(self, order_id:int, current_user:User, payload:OrderStatusUpdate)->OrderRead:
        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied"
            )
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        order.status = payload.status.value
        db_order = self.order_repository.update_order(order)
        return self._dump_order(db_order)






