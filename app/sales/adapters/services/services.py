import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.sales.adapters.serializers.sale_schema import ordersSchema, orderSchema
from app.sales.domain.pydantic.sale_pydantic import (
  ClientCreate, SaleCreate, SalesOrdersCreate, SalesOrders as SalesOrderPy
)
from app.sales.adapters.sqlalchemy.sale import Sale, Client, SalesOrders, StatusSale
from app.products.adapters.sqlalchemy.product import Product

session = ConectDatabase.getInstance()

def getGeneralClient() -> Client:
  client = session.scalars(select(Client).where(Client.name == "general")).one()
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
  return client

def GetAllSales(limit:int, skip:int = 0):
  sales = session.scalars(select(Sale).offset(skip).limit(limit)).all()
  if not sales:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sales not found")
  return sales

def GetSaleById(id:str) -> Sale:
  sale = session.get(Sale, id)
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  return sale

def CreateSale():
  client = getGeneralClient()
  new_sale = Sale(pyment_method="", type_sale="", id_client=client.id)
  session.add(new_sale)
  session.commit()
  session.refresh(new_sale)
  return new_sale

def AddOrder(id_sale: str, orders: list[SalesOrdersCreate]):
  if not orders:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orders not found")
  
  for order in orders:
    statement = select(Product).where(Product.id == order.product_id)
    product = session.scalars(statement).one()
  
    if not product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    
    price_total:float = product.sale_price * order.amount_product

    new_order = SalesOrders(sale_id=id_sale, product_id=order.product_id, amount_product=order.amount_product, total=price_total)
    session.add(new_order)
    session.commit()
    
  sale = session.get(Sale, uuid.UUID(id_sale))
  
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
  
  return {
    "message": "Orders added successfully"
  }

def ConfirmSale(id_sale: str, saleCreate: SaleCreate, orders: list[SalesOrdersCreate]):
  
  # We verify that the number of orders is greater that zero.
  if len(orders) <= 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orders required for confirm sale")
  
  
  AddOrder(id_sale, orders)
  # We verify that the type sale and payment method is different from empty.
  if saleCreate.type_sale == "" or saleCreate.payment_method == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the type of sale and the payment_method are required")
  
  # Get sale from database.
  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one()
  
  # We verify that the sale exists.
  if not sale:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sale not found")
  
  # We verify that the sale is not paid.
  # if sale.status == StatusSale.PAID:
  #   raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="sorry, you can't modify a sale")
  
  # If the sale is a "pedido", We will add the client, if not, we will add general client.
  if saleCreate.type_sale == "pedido":
    client = AddClient(saleCreate.client)
    sale.id_client = client.id
  else:
    generalClient = getGeneralClient()
    sale.id_client = generalClient.id
  
  # Consultamos todas las ordenes
  listOrders = session.scalars(select(SalesOrders).where(SalesOrders.sale_id == id_sale)).all()
  
  
  # We calculate the total
  total:float = 0.0
  for order in listOrders:
    total += order.total
  
  sale.amount_order = len(orders)
  sale.total = total
  sale.pyment_method = saleCreate.payment_method
  sale.type_sale = saleCreate.type_sale
  sale.status = StatusSale.PAID if saleCreate.type_sale == "fisico" else StatusSale.PENDING
  session.add(sale)
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


def ConfirmOrder(id_sale: str):
  sale = GetSaleById(id_sale)
  if sale.status == StatusSale.OPEN:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sale can't be modified")
  else:
    if sale.status == StatusSale.PENDING:
      sale.status = StatusSale.PAID
    