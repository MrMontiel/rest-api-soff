from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from app.sales.adapters.services.services import CreateSale, GetAllSales, AddClient, AddOrder

from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders, Client
from app.products.adapters.sqlalchemy.product import Product
from app.sales.adapters.serializers.sale_schema import saleSchema, salesSchema, orderSchema, ordersSchema, clientsSchema, clientSchema

from app.sales.domain.pydantic.sale_pydantic import SaleCreate, SalesOrdersCreate, ClientCreate


session = SessionLocal()

sales = APIRouter(
  prefix='/sales',
  tags=["Sales"]
)

@sales.get('/')
async def get_all_sales(limit: int = 100):
  sales = GetAllSales()
  return {
    "amount_sales": len(sales),
    "sales": salesSchema(sales)
  }

@sales.post('/add-client')
async def create_client(client: ClientCreate):
  new_client = AddClient(client)
  return {
    "id": new_client.id,
    "client": clientSchema(new_client)
  }

@sales.post('/')
async def create_sale(sale: SaleCreate):
  new_sale = CreateSale(sale)
  return {
    "id": new_sale.id,
    "message": "sale created successfully"
  }

@sales.post('/{id_sale}/add-order')
async def asociated_order(id_sale: str, order: SalesOrdersCreate):
  new_order = AddOrder(id_sale, order)
  return {
    "sale_id": new_order.sale_id,
    "product_id": new_order.product_id,
    "message": "order add successfully"
  }

@sales.put('/{id_sale}/confirm-sale')
async def confirm_sale(id_sale: str, saleCreate: SaleCreate):
  sale = AddOrder(id_sale, saleCreate)
  return {
    "id_sale": sale.id,
    "sale": saleSchema(sale)
  }