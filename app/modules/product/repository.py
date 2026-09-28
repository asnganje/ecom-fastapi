from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.modules.product.model import Product


class ProductRepository():
    def __init__(self, db: Session):
        self.db = db
    def get_all_products(self, page:int, limit:int,
                         category_id: int | None= None,
                         brand_name: str | None = None,
                         is_active: bool | None = None,
                         min_price: float | None = None,
                         max_price: float | None = None,
                         sort_price:str | None=None
                         ) -> tuple[list[Product], int]:


        statement = select(Product)
        count_statement = select(func.count()).select_from(Product)

        if category_id is not None:
            statement = statement.where(Product.category_id == category_id)
            count_statement = count_statement.where(Product.category_id == category_id)
        if brand_name is not None:
            brand_conditions = func.lower(Product.brand_name) == brand_name.lower()
            statement = statement.where(brand_conditions)
            count_statement = count_statement.where(brand_conditions)
        if is_active is not None:
            statement = statement.where(Product.is_active.is_(is_active))
            count_statement = count_statement.where(Product.is_active.is_(is_active))
        if min_price is not None:
            statement=statement.where(Product.price >= min_price)
            count_statement=count_statement.where(Product.price >= min_price)
        if max_price is not None:
            statement=statement.where(Product.price <= max_price)
            count_statement=count_statement.where(Product.price <= max_price)

        total = self.db.scalar(count_statement) or 0

        if sort_price == "asc":
            statement = statement.order_by(Product.price.asc())
        elif sort_price == "desc":
            statement = statement.order_by(Product.price.desc())
        else:
            statement = statement.order_by(Product.id.asc())

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

    def search(self, query:str)->list[Product]:
        search_term=f"%{query}%"
        statement = select(Product).where(
            or_(
                Product.name.ilike(search_term),
                Product.brand_name.ilike(search_term),
                Product.description.ilike(search_term)
                )
        ).order_by(Product.id.asc())
        return self.db.scalars(statement).all()

