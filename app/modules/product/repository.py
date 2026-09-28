from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.modules.product.model import Product


class ProductRepository():
    def __init__(self, db: Session):
        self.db = db
    def get_all_products(self, page:int, limit:int) -> tuple[list[Product], int]:
        statement = select(Product)
        count_statement = select(func.count()).select_from(Product)
        total = self.db.scalar(count_statement) or 0
        offset  = (page-1)*limit
        products = self.db.scalars(statement.offset(offset).limit(limit)).all()
        return products, total
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
