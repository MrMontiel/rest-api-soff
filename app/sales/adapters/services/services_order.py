from fastapi import status, HTTPException
from app.products.adapters.services.services import GetProductById, GetDetailsProduct
from app.supplies.adapters.services.services import GetOneSupply
from app.sales.domain.pydantic.sale_pydantic import (SalesOrdersCreate)
from app.supplies.domain.pydantic.supply import Supply
from app.products.domain.pydantic.product import RecipeDatail
from app.infrastructure.database import ConectDatabase
from app.supplies.adapters.sqlalchemy.supply import Supply as SupplySQLAlchemy
from app.sales.adapters.sqlalchemy.sale import SalesOrders
session = ConectDatabase.getInstance()

def SupplyAvailability(supply:Supply, detail:RecipeDatail) -> bool:
  if supply.quantity_stock < detail.amount_supply:
    return False
  return True

def UpdateStockSupply(supply: Supply, detail:RecipeDatail):
  supply_obt = session.get(SupplySQLAlchemy, supply.id)
  supply_obt.quantity_stock = supply_obt.quantity_stock - detail.amount_supply
  session.add(supply_obt)
  session.commit()
  session.refresh(supply_obt)
  return supply_obt

def OrderProcessing(order: SalesOrdersCreate):
  if not order:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content in order")
  product = GetProductById(order.product_id)
  details = GetDetailsProduct(product.id)
  counterOrder = 0
  for detail in details:
    supply = GetOneSupply(detail.supply_id)
    availability = SupplyAvailability(supply, detail)
    if availability == False:
      raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="order not added")
    UpdateStockSupply(supply, detail)
    counterOrder += 1
  return order

def AddOrder(order: SalesOrdersCreate):
  product = GetProductById(order.product_id)
  total = product.sale_price *  order.amount_product
  order_sqlalchemy = SalesOrders(sale_id=order.sale_id, product_id=order.product_id, amount_product=order.amount_product, total=total)
  session.add(order_sqlalchemy)
  session.commit()
  session.refresh(order_sqlalchemy)
  return order