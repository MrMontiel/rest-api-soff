from enum import Enum
from pydantic import BaseModel
from typing import Optional

class SupplyBase(BaseModel):
    name: str
    price: float
    quantity_stock: int
    unit_measure: str
    
class SupplyU(BaseModel):
    name: str
    price: float
    total: float
    quantity_stock: int
    unit_measure: str
    
class Supply(SupplyBase):
    id: Optional[str]
    total: Optional[float] 
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

class SupplyUpdate(SupplyU):
    
    pass

class SupplyDelete(SupplyBase):
    
    pass

