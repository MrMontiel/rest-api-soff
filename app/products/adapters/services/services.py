import uuid
from sqlalchemy import select, delete
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema, recipeDetailsSchema

session = ConectDatabase.getInstance()

def GetAllProducts(limit:int, offset:int):
  products = session.scalars(select(Product).offset(offset).limit(limit)).all()
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
  return products

def GetDetailsProduct(id_product):
  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = session.scalars(statement).all()
  if not details:
    return []
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details not found")
  return details
def GetProductById(id_product):
  product = session.get(Product, uuid.UUID(id_product))

  return product
  
def GetDetailsProduct(id_product: str):
  if not id_product:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id_product if required")

  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = session.scalars(statement).all()

  return details

def GetDetailById(id_detail):
  detail = session.get(RecipeDetail, uuid.UUID(id_detail))
  return detail

def CreateProduct ():
  new_product = Product(name="", sale_price=0)
  session.add(new_product)
  session.commit()
  session.refresh(new_product)
  return new_product

def AddDetail(id_product:str, detail: RecipeDetailCreate):
  statement = select(Supply).where(Supply.id == detail.supply_id)
  supply = session.scalars(statement).one()
  if not supply:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="supply not found")
  
  total:float = supply.price * detail.amount_supply

  product = session.scalars(select(Product).where(Product.id == id_product)).one() 

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  
  detail_added = session.scalars(select(RecipeDetail).where(RecipeDetail.product_id == id_product)).all()
  for n in detail_added:
    if n.supply_id == uuid.UUID(detail.supply_id):
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Supply is already registered")

  new_detail = RecipeDetail(product_id=id_product, supply_id=detail.supply_id, amount_supply=detail.amount_supply, unit_measure=detail.unit_measure, subtotal=total)
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
    total += detail.subtotal


  product = session.scalars(select(Product).where(Product.id == id_product)).one()

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
  
  product.name = productCreate.name
  product.price = total
  product.sale_price = productCreate.sale_price
  session.commit()
  session.refresh(product)
  return product

def UpdateDetail(id_detail:str, amount_supply:int):
  detail = GetDetailById(id_detail)

  if not detail:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="detail not found")
  
  detail.amount_supply = amount_supply
  detail.subtotal = detail.supply.price * amount_supply
  session.add(detail)
  session.commit()
  session.refresh(detail)
  return detail

def UpdateProduct(id_product: str, products:ProductCreate):
  product = GetProductById(id_product)

  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

  # if product.status:
  product.name = products.name
  product.sale_price = products.sale_price
  session.add(product)
  session.commit()
  session.refresh(product)
  return product
  
  # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot update inactive product")


def DeleteDetail(id_detail:str):
  detail = session.get(RecipeDetail, uuid.UUID(id_detail))
  # detail = session.scalars(select(RecipeDetail).where(RecipeDetail.id == id_detail)).one()

  if not detail:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")
  
  session.delete(detail)
  session.commit()

# def ChangeStatus(id_product:str):
#   product = session.get(Product, uuid.UUID(id_product))

#   if not product:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#   if product.status:
#     product.status = False
#     session.add(product) 
#     session.commit()

#   else:
#     product.status = True
#     session.add(product)
#     session.commit()
    



  