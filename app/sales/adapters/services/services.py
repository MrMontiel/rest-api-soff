import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.sales.adapters.serializers.sale_schema import ordersSchema, orderSchema
from app.sales.domain.pydantic.sale_pydantic import (
  ClientCreate, SaleCreate, SalesOrdersCreate
)
from app.sales.adapters.sqlalchemy.sale import Sale, Client, SalesOrders, StatusSale
from app.products.adapters.sqlalchemy.product import Product

session = SessionLocal()

def getGeneralClient() -> Client:
  client = session.scalars(select(Client).where(Client.name == "general")).one()
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
  return client

def GetAllSales(limit:int = 100):
  sales = session.scalars(select(Sale).limit(limit)).all()
  if not sales:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sales not found")
  return sales

def GetSaleById(id:str):
  sale = session.get(Sale, uuid.UUID(id))
  return sale

def CreateSale():
  client = getGeneralClient()
  new_sale = Sale(pyment_method="", type_sale="", id_client=client.id)
  session.add(new_sale)
  session.commit()
  session.refresh(new_sale)
  return new_sale

def AddOrder(id_sale: str, order: SalesOrdersCreate):
  statement = select(Product).where(Product.id == order.product_id)
  product = session.scalars(statement).one()
  
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  price_total:float = product.sale_price * order.amount_product

  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one() 
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
  order_added = session.scalars(select(SalesOrders).where(SalesOrders.sale_id == id_sale)).all()
  for n in order_added:
    if n.product_id == uuid.UUID(order.product_id):
      n.amount_product += order.amount_product
      n.total = n.amount_product * n.product.sale_price
      session.add(n)
      session.commit()
      session.refresh(n) 
      return n 
  new_order = SalesOrders(sale_id=id_sale, product_id=order.product_id, amount_product=order.amount_product, total=price_total)
  session.add(new_order)
  session.commit()
  session.refresh(new_order)
  return new_order

def ConfirmSale(id_sale: str, saleCreate: SaleCreate):
  statement = select(SalesOrders).where(SalesOrders.sale_id == id_sale)
  orders = ordersSchema(session.scalars(statement).all())
  
  if len(orders) <= 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orders required for confirm sale")
  
  total:float = 0.0
  
  for order in orders:
    total += order['total']
 
  if saleCreate.type_sale == "" or saleCreate.payment_method == "" or saleCreate.id_client == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the type of sale, the payment_method and client are required")
    
  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one()
  
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
  if sale.status == StatusSale.PAID:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="sorry, you can't modify a sale")

  sale.amount_order = len(orders)
  sale.total = total
  sale.pyment_method = saleCreate.payment_method
  sale.type_sale = saleCreate.type_sale
  sale.id_client = saleCreate.id_client
  sale.status = StatusSale.PAID if saleCreate.type_sale == "fisico" else StatusSale.PENDING
  session.commit()
  session.refresh(sale)
  return sale

def AddClient(client: ClientCreate):
  if not client:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="client is required")
  if client.email == "" or client.direction == "" or client.phone == "" or client.name == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the fields name, phone, direction and email are required")
  new_client = Client(name=client.name, direction=client.direction, phone=client.phone, email=client.email)
  session.add(new_client)
  session.commit()
  session.refresh(new_client)
  return new_client

def seeSalesOrders(id_sale: str):
  if not id_sale:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id_sale if required")
  statement = select(SalesOrders).where(SalesOrders.sale_id == id_sale)
  orders = session.scalars(statement).all()
  return orders

def GetClient(id: str):
  client = session.get(Client, uuid.UUID(id))
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
  return client



def UpdateAmountOrder(id_order: str, amount_product: int):
  order = session.get(SalesOrders, uuid.UUID(id_order))
  if not order:
    raise HTTPException(status_code=404, detail="not found order")
  print(order)
  order.amount_product = amount_product
  order.total = order.product.sale_price * amount_product
  session.add(order)
  session.commit()
  session.refresh(order)
  return order