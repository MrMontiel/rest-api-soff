from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PurchaseBase(BaseModel):
    id_provider: str

class Purchase(PurchaseBase):
    id: Optional[str]
    purchase_date: str
    amount_order: int=0
    total: float = 0.0
    status: bool = True
    
class Config:
    from_attributes = True
    
class PurchaseCreate(PurchaseBase):
    pass

class OrderPurchaseBase(BaseModel):
    id_supplies: str
    amount_supplies: int
    price_supplies: float
    id_purchase: str
    
class OrderPurchase(OrderPurchaseBase):
    id: Optional[str]
    subtotal: float

class Config:
    from_attributes = True
    
class OrderPurchaseCreate(OrderPurchaseBase):
    pass