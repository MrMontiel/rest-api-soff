import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.sales.adapters.serializers.sale_schema import ordersSchema, orderSchema
from app.sales.domain.pydantic.sale_pydantic import (
  ClientCreate, SaleCreate, SalesOrdersCreate
)
from app.sales.adapters.sqlalchemy.sale import Sale, Client, SalesOrders
from app.products.adapters.sqlalchemy.product import Product

session = SessionLocal()

def GetAllSales(limit:int = 100):
  sales = session.scalars(select(Sale)).all()
  print(sales)
  if not sales:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sales not found")
  return sales

def CreateSale(sale: SaleCreate):
  if not sale:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sale is required")
  if sale.type_sale == "" or sale.payment_method == "" or sale.id_client == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the type of sale, the payment_method and client are required")
  
  client = session.scalars(select(Client).where(Client.id == sale.id_client)).one()
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")

  new_sale = Sale(pyment_method=sale.payment_method, type_sale=sale.type_sale, id_client=uuid.UUID(sale.id_client))
  session.add(new_sale)
  session.commit()
  session.refresh(new_sale)
  return new_sale

def AddOrder(id_sale: str, order: SalesOrdersCreate):
  statement = select(Product).where(Product.id == order.product_id)
  product = session.scalars(statement).one()
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  price_total:float = product.price * order.amount_product

  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one() 
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
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
    
  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one()
  
  if sale.type_sale == "" or sale.payment_method == "" or sale.id_client == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the type of sale, the payment_method and client are required")

  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
  sale.amount_order = len(orders)
  sale.total = total
  sale.pyment_method = saleCreate.pyment_method
  sale.type_sale = saleCreate.type_sale
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

def CambiarEstado():
  pass