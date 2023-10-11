import uuid
from sqlalchemy import select, delete, desc
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

def GetAllPurchases(limit:int, offset:int):
  purchases = session.scalars(select(Purchase).where(Purchase.amount_order >0).offset(offset).limit(limit).order_by(desc(Purchase.purchase_date))).all()
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
  price_total:float = order.price_supplies * order.amount_supplies

  purchase = session.scalars(select(Purchase).where(Purchase.id == id_purchase)).one() 
  if not purchase:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchase not found")
  
  #  Restricciones despues de confirmar compra
  if purchase.total != 0.0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You can't add orders because the purchase is confirmed")
  
  order_added = session.scalars(select(PurchasesOrders).where(PurchasesOrders.purchase_id == id_purchase)).all()
  for n in order_added:
    if n.supply_id == uuid.UUID(order.supply_id):
      n.amount_supplies += order.amount_supplies
      n.subtotal = n.amount_supplies * n.price_supplies
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
    supplies = session.get(Supply, order['supply_id'])
    if supplies:
      supplies.quantity_stock += order['amount_supplies']
      if order['price_supplies']>supplies.price:
        supplies.price = order['price_supplies']
      else:
        supplies.price = supplies.price
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
  order.subtotal = order.price_supplies * amount_supplies
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

def DeletePurchaseByid(id_purchase:str):
  purchase = session.get(Purchase, uuid.UUID(id_purchase))
  print(purchase)
  if not purchase:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="purchase not found")
  
  #  Restricciones despues de confirmar compra
  if purchase.total != 0.0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You can't delete purchase because the purchase is confirmed")
  
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
  orders = ordersSchema(session.scalars(statement).all())
  
  if len(orders) > 0:
    delete_statement = delete(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
    session.execute(delete_statement)
  session.delete(purchase)
  session.commit()


# def ChangeStatus(id_purchase:str):
#   purchase = session.get(Purchase, uuid.UUID(id_purchase))

#   if not purchase:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
  
#   statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
#   orders = ordersSchema(session.scalars(statement).all())

#   for order in orders:
#     supplies = session.get(Supply, order['supply_id'])
#     if supplies:
#       supplies.quantity_stock -= order['amount_supplies']
#       session.commit()
#       session.refresh(supplies)

#   purchase.status = not purchase.status  
#   session.add(purchase)