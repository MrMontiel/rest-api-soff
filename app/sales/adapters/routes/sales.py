from sqlalchemy import select
from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException, status
from app.sales.adapters.services.services import (
  CreateSale, 
  GetAllSales, 
  AddClient, 
  AddOrder, 
  ConfirmSale, 
  seeSalesOrders, 
  getGeneralClient,
  GetSaleById,
  UpdateAmountOrder
  )
import uuid
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders, Client
from app.products.adapters.sqlalchemy.product import Product
from app.sales.adapters.serializers.sale_schema import saleSchema, salesSchema, orderSchema, ordersSchema, clientsSchema, clientSchema

from app.sales.domain.pydantic.sale_pydantic import SaleCreate, SalesOrdersCreate, ClientCreate

from app.products.adapters.sqlalchemy.product import Product
from app.products.adapters.serializers.product_schema import productSchema, productsSchema

from app.sales.adapters.routes.clients import clients

session = ConectDatabase.getInstance()

sales = APIRouter(
  prefix='/sales',
  tags=["Sales"]
)

sales.include_router(clients)

@sales.get('/products')
async def get_all_products():
  products = session.scalars(select(Product)).all()
  return productsSchema(products)

@sales.get('/clients')
async def get_all_products():
  clients = session.scalars(select(Client)).all()
  return clientsSchema(clients)

@sales.get('/client/general')
async def get_client_by_id():
  client = getGeneralClient()
  return client

@sales.get('/')
async def get_all_sales(limit: int = 100):
  sales = GetAllSales()
  return {
    "amount_sales": len(sales),
    "sales": salesSchema(sales)
  }

@sales.get('/{id_sale}')
async def get_sale_by_id(id_sale: str):
  sale = GetSaleById(id_sale)
  return saleSchema(sale)

@sales.post('/add-client')
async def create_client(client: ClientCreate):
  new_client = AddClient(client)
  return clientSchema(new_client)

@sales.post('/')
async def create_sale():
  new_sale = CreateSale()
  return {
    "id": new_sale.id,
    "message": "sale created successfully"
  }

@sales.post('/{id_sale}/add-order')
async def add_order(id_sale: str, order: SalesOrdersCreate):
  new_order = AddOrder(id_sale, order)
  return {
    "sale_id": new_order.sale_id,
    "product_id": new_order.product_id,
    "message": "order add successfully"
  }

@sales.put('/{id_sale}/confirm-sale')
async def confirm_sale(id_sale: str, saleCreate: SaleCreate):
  sale = ConfirmSale(id_sale, saleCreate)
  return {
    "id_sale": sale.id,
    "sale": saleSchema(sale)
  }
  
@sales.get('/{id_sale}/orders')
async def getAllOrdersBySaleId(id_sale: str):
  orders = seeSalesOrders(id_sale)
  return {
    "id_sale": id_sale,
    "orders": ordersSchema(orders)
  }
  
@sales.put('/update-amount-order')
async def UpdateAmountOrderBySaleId(id_order:str, amount_product: int):
  order = UpdateAmountOrder(id_order, amount_product)
  return orderSchema(order)


@sales.delete('/{id_order}/delete')
async def DeleteOrderById(id_order: str):
  order = session.get(SalesOrders, uuid.UUID(id_order))
  if not order:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
  session.delete(order)
  session.commit()
  return {
    "message": "Order deleted successfully"
  }