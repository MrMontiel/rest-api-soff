from enum import Enum
from pydantic import BaseModel
from typing import Optional

class SupplyBase(BaseModel):
    name: str
    price: float
    quantity_stock: int
    unit_measure: str
    
class Supply(SupplyBase):
    id: Optional[str]
    status: bool = True
    
    class Config:
        from_attributes = True
    
class SupplyCreate(SupplyBase):
    
    pass