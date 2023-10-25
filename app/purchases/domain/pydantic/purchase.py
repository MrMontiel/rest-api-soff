from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PurchaseBase(BaseModel):
    purchase_date: str
    provider_id: str
    invoice_number: str

class PurchasesConfirm(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: Optional[str]
    purchase_date: str
    amount_order: int=0
    total: float = 0.0
    
class Config:
    from_attributes = True
    
class PurchaseCreate(PurchaseBase):
    pass

class OrderPurchaseBase(BaseModel):
    supply_id: str
    amount_supplies: int
    price_supplies: float
    purchase_id: str
    
class OrderPurchase(OrderPurchaseBase):
    id: Optional[str]
    subtotal: float

class Config:
    from_attributes = True
    
class OrderPurchaseCreate(OrderPurchaseBase):
    pass