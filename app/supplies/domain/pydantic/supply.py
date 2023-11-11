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
    total: float
    status: bool = True
    
    class Config:
        from_attributes = True
    
class SupplyCreate(BaseModel):
    name: str
    price: float
    quantity_stock: int
    unit_measure: str
    
    # def convert_to_grams(self):
    #     if self.unit_measure == 'Kilogramos':
    #         self.unit_measure == "Gramos"
    #         self.quantity_stock *= 1000 

class SupplyUpdate(SupplyBase):
    
    pass

class SupplyDelete(SupplyBase):
    
    pass

