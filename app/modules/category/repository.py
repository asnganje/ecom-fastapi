from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.category.model import Category


class CategoryRepository():
    def __init__(self, db: Session)->None:
        self.db = db
    def get_all_categories(self)->list[Category]:
        statement = select(Category).order_by(Category.id)
        return self.db.scalars(statement).all()
    def get_category_by_id(self, category_id: int)->Category | None:
        return self.db.get(Category, category_id)
    def create_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    def update_category(self, category:Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category
    def delete_category(self, category: Category) ->None:
        self.db.delete(category)
        self.db.commit()
