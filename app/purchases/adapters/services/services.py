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
from app.purchases.adapters.exceptions.exceptions import PurchaseNotFound,NotConfirmPurchaseInvoiceExist,NotConfirmPurchase,NotDeletePurchaseConfirm,OrderNotFound,IdPurchaseRequired,OrderRequiredForConfirm,PurchaseConfirm,SupplyNotFound,PurchasesNotFound,ProviderNotFound

session = ConectDatabase.getInstance()

def getGeneralProvider() -> Provider:
  provider = session.scalars(select(Provider).where(Provider.name == "general")).one()
  if not provider:
    ProviderNotFound()
  return provider

def GetAllPurchases(limit:int, offset:int=0):
  purchases = session.scalars(select(Purchase).offset(offset).limit(limit).order_by(desc(Purchase.purchase_date))).all()
  if not purchases:
    PurchasesNotFound()
  return purchases

def GetPurchaseById(id:str) -> Purchase:
  purchase = session.get(Purchase, id)
  if not purchase:
    PurchaseNotFound()
  return purchase

def CreatePurchase():
  provider = getGeneralProvider()
  new_purchase = Purchase(provider_id= provider.id, invoice_number= "")
  session.add(new_purchase)
  session.commit()
  session.refresh(new_purchase)
  return new_purchase

def AddOrder(id_purchase: str, order: OrderPurchaseCreate):
  statement = select(Supply).where(Supply.id == order.supply_id)
  supply = session.scalars(statement).one()
  
  if not supply:
    SupplyNotFound()
  price_total:float = order.price_supplies * order.amount_supplies

  purchase = session.scalars(select(Purchase).where(Purchase.id == id_purchase)).one() 
  if not purchase:
    PurchaseNotFound()
  
  #  Restricciones despues de confirmar compra
  if purchase.total != 0.0:
    PurchaseConfirm()
  
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

def ConfirmPurchase(id_purchase: str, purchase_date:str,id_provider: str, invoice_number: str):
  
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
  orders = ordersSchema(session.scalars(statement).all())
  
  if len(orders) <= 0:
    OrderRequiredForConfirm()
  
  total:float = 0.0
  
  for order in orders:
    total += order['subtotal']
    supplies = session.get(Supply, order['supply_id'])
    if supplies:
      if supplies.unit_measure == 'Gramos':
        convert = (order['amount_supplies'])*1000
        supplies.quantity_stock += convert
        convertprice = (order['price_supplies'])/1000
        supplies.price = (supplies.price + convertprice)/2
        supplies.total = supplies.quantity_stock * supplies.price
      else:
        supplies.quantity_stock += order['amount_supplies']
        average = (supplies.price + order['price_supplies'])/2
        supplies.price = average
        supplies.total = supplies.quantity_stock * supplies.price
    session.commit()
    session.refresh(supplies)
    
 
  purchase = session.scalars(select(Purchase).where(Purchase.id == id_purchase)).one()
  invoice = session.scalars(select(Purchase.invoice_number)).all()

  if not purchase:
    PurchaseNotFound()

  if invoice_number in invoice:
    NotConfirmPurchaseInvoiceExist()
  

  purchase.amount_order = len(orders)
  purchase.total = total
  purchase.purchase_date = purchase_date
  purchase.provider_id = uuid.UUID(id_provider)
  purchase.invoice_number = invoice_number
  session.commit()
  session.refresh(purchase)
  return purchase


def seePurchasesOrders(id_purchase: str):
  if not id_purchase:
    IdPurchaseRequired()
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == id_purchase)
  orders = session.scalars(statement).all()
  return orders

def UpdateAmountOrder(id_order: str, amount_supplies: int):
  order = session.get(PurchasesOrders, uuid.UUID(id_order))
  if not order:
    OrderNotFound()
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
    OrderNotFound()
  session.delete(order)
  session.commit()

def DeletePurchaseByid(id_purchase:str):
  purchase = session.get(Purchase, uuid.UUID(id_purchase))
  print(purchase)
  if not purchase:
    PurchaseNotFound()
  
  #  Restricciones despues de confirmar compra
  if purchase.total != 0.0:
    NotDeletePurchaseConfirm()
  
  statement = select(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
  orders = ordersSchema(session.scalars(statement).all())
  
  if len(orders) > 0:
    delete_statement = delete(PurchasesOrders).where(PurchasesOrders.purchase_id == uuid.UUID(id_purchase))
    session.execute(delete_statement)
  session.delete(purchase)
  session.commit()
