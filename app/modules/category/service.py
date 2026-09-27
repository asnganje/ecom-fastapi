from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.testing import exclude

from app.modules.category.model import Category
from app.modules.category.repository import CategoryRepository
from app.modules.category.schema import CategoryRead, CategoryCreate, CategoryUpdate


class CategoryService():
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)
    def _dump_category(self, category: Category) ->CategoryRead:
        return CategoryRead.model_validate(category).model_dump()
    def list_categories(self)->list[CategoryRead]:
        categories = self.repository.get_all_categories()
        results = [self._dump_category(category) for category in categories]
        return results
    def get_category(self, category_id:int)->CategoryRead:
        category = self.repository.get_category_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        result = self._dump_category(category)
        return result

    def create_category(self, category:Category)->CategoryCreate:
        if category.parent_id is not None:
            parent_category = self.repository.get_category_by_id(category.id)
            if parent_category is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category already exists!"
                )
        db_Category = Category(**category.model_dump())
        saved_category = self.repository.create_category(db_Category)
        return self._dump_category(saved_category)

    def update_category(self, category_id:int, payload: CategoryUpdate)->CategoryRead:
        category = self.repository.get_category_by_id(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )
        changes = payload.model_dump(exclude_unset=True)
        if "parent_id" in changes:
            parent_id = changes["parent_id"]
            if parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Parent id and category id cannot be the same"
                )
            parent_category = self.repository.get_category_by_id(parent_id)
            if parent_category in None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found"
                )
        for field, value in changes.items():
            setattr(category, field, value)
        updated_category = self.repository.update_category(category)
        return self._dump_category(updated_category)
    def delete_category(self, category_id:int) -> None:
        db_category = self.repository.get_category_by_id(category_id)
        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        self.repository.delete_category(db_category)






