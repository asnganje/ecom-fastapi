from pydantic import BaseModel

class CategoryBase(BaseModel):
    name:str
    description:str
    parent_id:int | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name:str|None=None
    description:str|None=None
    parent_id:int|None=None


class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True
