import uuid
from sqlalchemy import select
from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException, status
from app.sales.adapters.services.services import ( CreateSale,  GetAllSales,  ConfirmSale,  seeSalesOrders,  getGeneralClient, GetSaleById, UpdateAmountOrder, ConfirmOrder, CancelSale )
from app.sales.adapters.services.services_order import AddOrder, OrderProcessing
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders, Client, StatusSale, VoucherSale
from app.products.adapters.sqlalchemy.product import Product
from app.sales.adapters.serializers.sale_schema import saleSchema, salesSchema, orderSchema, ordersSchema, clientsSchema, clientSchema
from fastapi import Depends
from app.sales.domain.pydantic.sale_pydantic import SaleCreate, SalesOrdersCreate, ClientCreate, VoucherCreate

from app.products.adapters.sqlalchemy.product import Product
from app.products.adapters.serializers.product_schema import productSchema, productsSchema
from app.auth.adapters.services.user import User, getCurrentActivateUser
session = ConectDatabase.getInstance()

sales = APIRouter(
  prefix='/sales',
  tags=["Sales"]
)

@sales.get('/client/general')
async def get_client_by_id():
  client = getGeneralClient()
  return client

@sales.get('/')
async def get_all_sales(limit: int = 100, skip:int = 0, user: User = Depends(getCurrentActivateUser)):
  sales = GetAllSales(limit, skip)
  return salesSchema(sales)
  

@sales.get('/{id_sale}')
async def get_sale_by_id(id_sale: str, user: User = Depends(getCurrentActivateUser)):
  sale = GetSaleById(id_sale)
  return saleSchema(sale)

# @sales.post('/add-client')
# async def create_client(client: ClientCreate):
#   new_client = AddClient(client)
#   return clientSchema(new_client)

@sales.post('/')
async def create_sale():
  new_sale = CreateSale()
  return {
    "id": new_sale.id,
    "message": "sale created successfully"
  }

@sales.post('/{id_sale}/add-order')
async def add_order(id_sale: str, order_created:SalesOrdersCreate):
  order = OrderProcessing(order_created)
  order_added = AddOrder(order)
  return {
    "message": "orders added successfully",
    "order": order_added
  }

class confirmSaleOrders:
  sale: SaleCreate
  orders: list[SaleCreate]

@sales.put('/{id_sale}/confirm-sale')
async def confirm_sale(id_sale: str, sale:SaleCreate):
  sale = ConfirmSale(id_sale, sale)
  return {
    "id_sale": sale.id,
    "sale": saleSchema(sale)
  }
  
@sales.get('/{id_sale}/orders')
async def getAllOrdersBySaleId(id_sale: str):
  orders = seeSalesOrders(id_sale)
  return ordersSchema(orders)

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
  
@sales.put('/{id_sale}/confirm-order')
async def ConfirmOrder(id_sale: str):
  ConfirmOrder(id_sale)
  pass

@sales.post('/{id_sale}/confirm-pending')
async def ConfirmSalePending(id_sale: str, voucher_create: VoucherCreate):
  sale = session.get(Sale, uuid.UUID(id_sale))
  voucher = VoucherSale(filename=voucher_create.filename, link=voucher_create.link, sale_id=id_sale)
  # Add voucher
  session.add(voucher)
  session.commit() 
  session.refresh(voucher)
  sale.status = StatusSale.PAID
  session.add(sale)
  session.commit()
  session.refresh(sale)
  return {
    "message" : "voucher added successfully"
  }



@sales.delete("/{id_sale}/cancel-sale")
async def CancelSaleById(id_sale: str):
  CancelSale(id_sale)
  return {
    "message": "Sale deleted successfully"
  }