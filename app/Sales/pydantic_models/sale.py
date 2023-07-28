from pydantic import BaseModel
from typing import Optional


class SaleBase(BaseModel):
  pyment_method: str
  type_sale: str
  
class Sale(SaleBase):
  id: Optional[str]
  sale_date: Optional[str]
  amount_orders: int = 0
  total: float = 0.0
  status: bool = True
  
  class Config:
    from_attributes = True
    
class SaleCreate(SaleBase):
  pass

class SalesOrdersBase(BaseModel):
  sale_id: str
  product_id: str
  amount_product: int
  
class SalesOrdersCreate(SalesOrdersBase):
  pass

class SalesOrders(SalesOrdersBase):
  id: Optional[str]
  total: float = 0.0
  
  class Config:
    from_attributes = True