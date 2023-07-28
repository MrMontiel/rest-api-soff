from fastapi import APIRouter, HTTPException, status
from app.config.database import SessionLocal
from sqlalchemy import select

from app.Sales.sqlalchemy_models.sale import Sale, SalesOrders, ProductFail
from app.Sales.schemas_models.sale import saleSchema, salesSchema, orderSchema, ordersSchema
from app.Sales.schemas_models.product import productSchema, productsSchema


from app.Sales.pydantic_models.sale import SaleCreate, SalesOrdersCreate


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

@sales.get('/products')
async def get_all_products(limit: int = 100):
  statement = select(ProductFail).limit(limit)
  products = session.scalars(statement).all()
  return {
    "count": len(products),
    "sales": productsSchema(products)
  }

@sales.post('/')
async def create_sale(sale: SaleCreate):
  if not sale:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sale not created")
  new_sale = Sale(pyment_method=sale.pyment_method, type_sale=sale.type_sale)
  session.add(new_sale)
  session.commit()
  return {
    "message": "sale created successfully"
  }

@sales.post('/{id_sale}/associate-order')
async def asociated_order(id_sale: str, order: SalesOrdersCreate):
  statement = select(ProductFail).where(ProductFail.id == order.product_id)
  product = session.scalars(statement).one()
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  price_total:float = product.price * order.amount_product
  new_order = SalesOrders(sale_id=id_sale, product_id=order.product_id, amount_product=order.amount_product, total=price_total)
  session.add(new_order)
  session.commit()
  return {
    "message": "order add successfully"
  }

@sales.put('/{id_sale}/confirm-sale')
async def confirm_sale(id_sale: str, saleCreate: SaleCreate):
  statement = select(SalesOrders).where(SalesOrders.sale_id == id_sale)
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