from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.product.model import Product


class ProductRepository():
    def __init__(self, db: Session):
        self.db = db
    def get_all_products(self) -> list[Product]:
        statement = select(Product).order_by(Product.id)
        return self.db.scalars(statement).all()
    def get_product_by_id(self, product_id:int)->Product | None:
        return self.db.get(Product, product_id)
    def create_product(self, product:Product)->Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    def update_product(self, product:Product)->Product:
        self.db.commit()
        self.db.refresh(product)
        return product
    def delete_product(self, product:Product)->None:
        self.db.delete(product)
        self.db.commit()
