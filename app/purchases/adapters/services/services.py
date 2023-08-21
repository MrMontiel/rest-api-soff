import uuid
from sqlalchemy import select, delete
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.purchases.adapters.serializers.purchase_schema import ordersSchema, orderSchema
from app.supplies.adapters.serializers.supply_schema import suppliesSchema, SupplySchema
from app.purchases.domain.pydantic.purchase import (
  PurchaseCreate, OrderPurchaseCreate
)
from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.providers.adapters.sqlachemy.provider import Provider

session = ConectDatabase.getInstance()

def getGeneralProvider() -> Provider:
  provider = session.scalars(select(Provider).where(Provider.name == "general")).one()
  if not provider:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="provider not found")
  return provider

def GetAllPurchases(limit:int):
  purchases = session.scalars(select(Purchase).limit(limit)).all()
  if not purchases:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchases not found")
  return purchases

def GetPurchaseById(id:str):
  purchase = session.get(Purchase, uuid.UUID(id))
  return purchase

def CreatePurchase():
  provider = getGeneralProvider()
  new_purchase = Purchase(provider_id= provider.id)
  session.add(new_purchase)
  session.commit()
  session.refresh(new_purchase)
  return new_purchase

def AddOrder(id_purchase: str, order: OrderPurchaseCreate):
  statement = select(Supply).where(Supply.id == order.supply_id)
  supply = session.scalars(statement).one()
  
  if not supply:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="supply not found")
  price_total:float = supply.price * order.amount_supplies

  purchase = session.scalars(select(Purchase).where(Purchase.id == id_purchase)).one() 
  if not purchase:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchase not found")
  
  order_added = session.scalars(select(PurchasesOrders).where(PurchasesOrders.purchase_id == id_purchase)).all()
  for n in order_added:
    if n.supply_id == uuid.UUID(order.supply_id):
      n.amount_supplies += order.amount_supplies
      n.total = n.amount_supplies * n.supply.price
      session.add(n)
      session.commit()
      session.refresh(n) 
      return n 
  new_order = PurchasesOrders(purchase_id=id_purchase, supply_id=order.supply_id, amount_supplies=order.amount_supplies,price_supplies=order.price_supplies, subtotal=price_total)
  session.add(new_order)
  session.commit()
  session.refresh(new_order)
  return new_order

def ConfirmPurchase(id_purchase: str, id_provider: str):
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
  orders = ordersSchema(session.scalars(statement).all())
  
  if len(orders) <= 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orders required for confirm purchase")
  
  total:float = 0.0
  
  for order in orders:
    total += order['subtotal']
    supplies = session.get(Supply, uuid.UUID(order['supply_id']) )
    if supplies:
      supplies.quantity_stock += order.amount_supplies
      supplies.price = order.price_supplies
      session.commit()
      session.refresh(supplies)
    
 
  purchase = session.scalars(select(Purchase).where(Purchase.id == id_purchase)).one()
  
  if not purchase:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchase not found")

  purchase.amount_order = len(orders)
  purchase.total = total
  purchase.provider_id = uuid.UUID(id_provider)
  session.commit()
  session.refresh(purchase)
  return purchase


def seePurchasesOrders(id_purchase: str):
  if not id_purchase:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id_purchase if required")
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == id_purchase)
  orders = session.scalars(statement).all()
  return orders

def UpdateAmountOrder(id_order: str, amount_supplies: int):
  order = session.get(PurchasesOrders, uuid.UUID(id_order))
  if not order:
    raise HTTPException(status_code=404, detail="not found order")
  print(order)
  order.amount_supplies = amount_supplies
  order.subtotal = order.supply.price * amount_supplies
  session.add(order)
  session.commit()
  session.refresh(order)
  return order

def DeleteOrderById(id_order: str):
  order = session.get(PurchasesOrders, uuid.UUID(id_order))
  print(order)
  if not order:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
  session.delete(order)
  session.commit()