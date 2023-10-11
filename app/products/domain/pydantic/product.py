from pydantic import BaseModel
from typing import Optional

class ProductBase (BaseModel):
    name: str
    sale_price: float

class Product(ProductBase):
    id: Optional[str]
    price: float
    register_date: str
    status: bool = True

    class Config:
        from_attributes = True
    
class ProductCreate(ProductBase):
  pass

class RecipeDetailBase(BaseModel):
    product_id: str
    supply_id: str
    amount_supply: int
    # unit_measure:str

class RecipeDetailCreate(RecipeDetailBase):
    pass

class RecipeDatail(RecipeDetailBase):
    id: Optional[str]
    subtotal: float

    class Config:
        from_attribute = True

