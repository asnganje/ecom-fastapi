from pydantic import BaseModel

class CategoryBase(BaseModel):
    name:str
    description:str
    parent_id:int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name:str|None
    description:str|None
    parent_id:int|None


class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True
