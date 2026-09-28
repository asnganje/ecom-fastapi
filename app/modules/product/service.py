from math import ceil
from unittest import result

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.product.model import Product
from app.modules.product.repository import ProductRepository
from app.modules.product.schema import ProductRead, ProductUpdate, ProductCreate
from app.common.price import calculate_selling_price


class ProductService():
    def __init__(self, db:Session):
        self.repository = ProductRepository(db)
    def _serialize_product(self, product:Product) -> ProductRead:
        payload = ProductRead.model_validate(product)
        payload.selling_price = calculate_selling_price(payload.price, payload.discount_percent)
        return payload
    def get_all_products(self, page:int, limit:int)->dict:
        products, total = self.repository.get_all_products(page, limit)
        results = [self._serialize_product(product) for product in products]
        return {
            "products":results,
            "pagination":{
                "page":page,
                "limit":limit,
                "total":total,
                "total_pages":ceil(total/limit)
            }
        }
    def get_product(self, product_id:int) -> ProductRead:
        product = self.repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!"
            )
        prod_output = self._serialize_product(product)
        return prod_output
    def create_product(self, product:ProductCreate) -> ProductRead:
        db_product = Product(**product.model_dump())
        saved_product = self.repository.create_product(db_product)
        return self._serialize_product(saved_product)
    def update_product(self, product_id, payload:ProductUpdate) -> ProductRead:
        db_product = self.repository.get_product_by_id(product_id)
        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!"
            )
        changes = payload.model_dump(exclude_none=True, exclude_unset=True)
        for field,value in changes.items():
            setattr(db_product, field, value)
        updated_product = self.repository.update_product(db_product)
        return self._serialize_product(updated_product)
    def delete_product(self, product_id) -> None:
        db_product = self.repository.get_product_by_id(product_id)
        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product not found"
            )
        self.repository.delete_product(db_product)


