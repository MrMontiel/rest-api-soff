from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema, recipeDetailsSchema

session = SessionLocal()

products = session.scalars(select(Product)).all()

def GetAllProducts(limit:int = 100):
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="products not found")
  return products

def GetDetailsProduct(id_product):
  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = session.scalars(statement).all()
  return details

def GetProductById(id_product):
  product = session.scalars(select(Product).where(Product.id == id_product)).one() 
  return product

def CreateProduct (product: ProductCreate):
  if not product:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product is required")
  if product.name == "" or product.sale_price == 0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name's product and price's product is required")
  
  new_product = Product(name=product.name, sale_price=product.sale_price)
  session.add(new_product)
  session.commit()
  session.refresh(new_product)
  return new_product

def AddDetail(id_product:str, detail: RecipeDetailCreate):
  supply = session.scalars(select(Supply).where(Supply.id == detail.supply_id)).one()

  if not supply:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="supply not found")
  
  product = GetProductById(id_product)

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  
  subtotal:float = supply.price * detail.amount_supply

  new_detail = RecipeDetail(product_id=id_product, supply_id=detail.supply_id, amount_supply=detail.amount_supply, unit_measure=detail.unit_measure, subtotal=subtotal)
  session.add(new_detail)
  session.commit()
  session.refresh(new_detail)
  return new_detail

def ConfirmProduct(id_product:str, productCreate:ProductCreate):
  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = recipeDetailsSchema(session.scalars(statement).all())

  if len(details) <= 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="details required for confirm product")
  
  total:float = 0.0

  for detail in details:
    total += detail['subtotal']

  if productCreate.name == "" or productCreate.sale_price == 0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name's product and price's product is required")
  
  product = GetProductById(id_product)

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

  product.name = productCreate.name
  product.price = total
  product.sale_price = productCreate.sale_price
  session.commit()
  session.refresh(product)
  return product


def UpdateDetail(id_product:str, id_supply:str, recipeDetailCreate:RecipeDetailCreate):
  details = session.scalars(select(RecipeDetail).where(RecipeDetail.product_id == id_product)).all()

  if len(details) <= 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="details required for confirm product")
  
  if recipeDetailCreate.amount_supply == 0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The amount supply is required")
  
  supply = session.scalars(select(RecipeDetail).where(RecipeDetail.product_id == id_product)).all() 
    
  supply.amount_supply = recipeDetailCreate.amount_supply
  session.commit()
  session.refresh(supply)
  return supply
