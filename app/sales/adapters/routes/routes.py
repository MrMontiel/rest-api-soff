from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from app.sales.adapters.services.services import CreateSale

from app.sales.adapters.sqlalchemy.sale import Sale, Association, Product, Client
from app.sales.adapters.serializers.sale_schema import saleSchema, salesSchema, orderSchema, ordersSchema, clientsSchema, clientSchema
from app.sales.adapters.serializers.product import productSchema, productsSchema

from app.sales.domain.pydantic.sale_pydantic import SaleCreate, SalesOrdersCreate, ClientCreate


session = SessionLocal()

sales = APIRouter(
  prefix='/sales',
  tags=["Sales"]
)

@sales.get('/')
async def get_all_sales(limit: int = 100):
  statement = select(Sale).limit(limit)
  sales = session.scalars(statement).all()
  return {
    "count": len(sales),
    "sales": salesSchema(sales)
  }

@sales.post('/create_client')
async def create_client(client: ClientCreate):
  new_client = Client(name=client.name, direction=client.direction, phone=client.phone, email=client.email)
  session.add(new_client)
  session.commit()
  session.refresh(new_client)
  return {
    "client": clientSchema(new_client)
  }

@sales.get('/products')
async def get_all_products(limit: int = 100):
  statement = select(Product).limit(limit)
  products = session.scalars(statement).all()
  return {
    "count": len(products),
    "products": productsSchema(products)
  }

@sales.post('/')
async def create_sale(sale: SaleCreate):
  new_sale = CreateSale(sale)
  return {
    "id": new_sale.id,
    "message": "sale created successfully"
  }

@sales.post('/{id_sale}/associate-order')
async def asociated_order(id_sale: str, order: SalesOrdersCreate):
  statement = select(Product).where(Product.id == order.product_id)
  product = session.scalars(statement).one()
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  price_total:float = product.price * order.amount_product
  new_order = Association(sale_id=id_sale, product_id=order.product_id, amount_product=order.amount_product, total=price_total)
  session.add(new_order)
  session.commit()
  return {
    "message": "order add successfully"
  }

@sales.put('/{id_sale}/confirm-sale')
async def confirm_sale(id_sale: str, saleCreate: SaleCreate):
  statement = select(Association).where(Association.sale_id == id_sale)
  orders = ordersSchema(session.scalars(statement).all())
  total:float = 0.0
  for order in orders:
    total += order['total']
  sale = session.scalars(select(Sale).where(Sale.id == id_sale)).one()
  if sale:
    sale.amount_order = len(orders)
    sale.total = total
    sale.pyment_method = saleCreate.pyment_method
    sale.type_sale = saleCreate.type_sale
    session.commit()
    session.refresh(sale)
  return {
    "id_sale": id_sale,
    "sale": sale 
  }