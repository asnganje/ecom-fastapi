from pydantic import BaseModel, Field

class SpecificationItem(BaseModel):
    name:str
    value:str

class SpecificationSection(BaseModel):
    section:str
    features:list[SpecificationItem]

class ProductBase(BaseModel):
    name:str
    brand_name:str
    model_number:str
    description:str
    warranty:str
    discount_percent:float= Field(ge=0, le=100)
    stock_quantity: int = Field(ge=0)
    is_active:bool = Field(default=True)
    price:float = Field(gt=0)
    image_url:str
    additional_images:list[str]
    category_id:int
    highlights:list[str]
    specifications:list[SpecificationSection]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name:str | None
    brand_name:str | None
    model_number:str | None
    description:str | None
    warranty:str | None
    discount_percent:float= Field(ge=0, le=100) | None
    stock_quantity: int = Field(ge=0) | None
    is_active:bool = Field(default=True)
    price:float = Field(gt=0) | None
    image_url:str | None
    additional_images:list[str] | None
    category_id:int | None
    highlights:list[str] | None
    specifications:list[SpecificationSection] | None

class ProductRead(ProductBase):
    id:int
    selling_price: float|None
    class Config:
        from_attributes = True