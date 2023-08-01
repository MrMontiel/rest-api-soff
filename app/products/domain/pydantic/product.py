from pydantic import BaseModel
from typing import Optional

class ProductBase (BaseModel):
    name: str
    price: float
    sale_price: float

class Product(ProductBase):
    id: Optional[str]
    status: bool = True

    class Config:
        from_attributes = True
    
class ProductCreate(ProductBase):
  pass

class RecipeDetailBase(BaseModel):
    product_id: str
    supply_id: str
    amount_supply: int
    unit_measure:str

class RecipeDatail(RecipeDetailBase):
    id: Optional[str]

    class Config:
        from_attribute = True

class RecipeDetailCreate(RecipeDetailBase):
    pass