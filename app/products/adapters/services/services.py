import uuid
from sqlalchemy import select, delete, desc, asc
from fastapi import status, HTTPException
from app.products.adapters.exceptions.exceptions import (
  ProductNotFound,
  ProductsNotFound,  
  IdProductRequired,
  SupplyNotFound,
  ProductNotUpdate,
  DetailsRequired,
  InfoProductRequired,
  NameProductExist,
  DetailNotFound
  )
from app.infrastructure.database import ConectDatabase
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema, recipeDetailsSchema

session = ConectDatabase.getInstance()

def GetAllProducts(limit:int, offset:int):
  products = session.scalars(select(Product).offset(offset).limit(limit)).all()
  if not products:
    ProductsNotFound()
  return products

def GetDetailsProduct(id_product:str):
  if not id_product:
    IdProductRequired()

  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = session.scalars(statement).all()
  return details

def GetProductById(id_product:str) ->Product:
  product = session.get(Product, id_product)
  if not product:
    ProductNotFound()
  return product

def CreateProduct ():
  new_product = Product(name="", sale_price=0.0)
  session.add(new_product)
  session.commit()
  session.refresh(new_product)
  return new_product

def AddDetail(id_product:str, detail: RecipeDetailCreate):
  statement = select(Supply).where(Supply.id == detail.supply_id)
  supply = session.scalars(statement).one()

  if not supply:
    SupplyNotFound()
    
  total:float = supply.price * detail.amount_supply

  product = session.scalars(select(Product).where(Product.id == id_product)).one() 

  if not product:
    ProductNotFound()

  if product.status:
    detail_added = session.scalars(select(RecipeDetail).where(RecipeDetail.product_id == id_product)).all()
  
    for n in detail_added:
      if n.supply_id == uuid.UUID(detail.supply_id):
        n.amount_supply += detail.amount_supply
        n.subtotal = n.amount_supply * supply.price
        session.add(n)
        session.commit()
        session.refresh(n) 
        return n 

    new_detail = RecipeDetail(product_id=id_product, supply_id=detail.supply_id, amount_supply=detail.amount_supply, subtotal=total)
    session.add(new_detail)
    session.commit()
    session.refresh(new_detail)
    return new_detail
  
  ProductNotUpdate()

def ConfirmProduct(id_product:str, productCreate:ProductCreate): 
  product = GetProductById(id_product)

  if product.status:
    product_name = session.scalars(select(Product.name)).all()

    if productCreate.name in product_name:
      NameProductExist()

    if productCreate.name == "" or productCreate.sale_price == 0:
      InfoProductRequired()

    if not product:
      ProductNotFound()

    statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
    details = recipeDetailsSchema(session.scalars(statement).all())

    if len(details) <= 0:
      DetailsRequired()

    total:float = 0.0

    for detail in details:
      total += detail['subtotal']

    product.name = productCreate.name
    product.price = total
    product.sale_price = productCreate.sale_price
    session.commit()
    session.refresh(product)
    return product
  
  ProductNotUpdate()

def UpdateDetail(id_detail:str, amount_supply:int):
  detail = session.get(RecipeDetail, uuid.UUID(id_detail))

  if not detail:
    DetailNotFound()

  detail.amount_supply = amount_supply
  detail.subtotal = detail.supply.price * amount_supply
  session.add(detail)
  session.commit()
  session.refresh(detail)
  return detail

def UpdateProduct(id_product: str, products:ProductCreate):
  product_name = session.scalars(select(Product.name)).all()

  # if products.name in product_name:
  #   NameProductExist()

  if products.name == "" or products.sale_price == 0:
    InfoProductRequired()
  
  product = GetProductById(id_product)

  if not product:
    ProductNotFound()

  statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
  details = recipeDetailsSchema(session.scalars(statement).all())

  if len(details) <= 0:
    DetailsRequired()
    
  total:float = 0.0

  for detail in details:
    total += detail['subtotal']

  if product.status:
    product.name = products.name
    product.price = total
    product.sale_price = products.sale_price
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
  
  ProductNotUpdate()

def DeleteDetail(id_detail:str):
  detail = session.get(RecipeDetail, uuid.UUID(id_detail))

  if not detail:
    DetailNotFound()

  session.delete(detail)  
  session.commit()

def DeleteProduct(id_product:str):
  product = session.get(Product, uuid.UUID(id_product))

  if not product:
    ProductNotFound()

  statement = select(RecipeDetail).where(RecipeDetail.product_id == uuid.UUID(id_product))
  details = recipeDetailsSchema(session.scalars(statement).all())
  
  if len(details) > 0:
    delete_statement = delete(RecipeDetail).where(RecipeDetail.product_id == uuid.UUID(id_product))
    session.execute(delete_statement)

  session.delete(product)
  session.commit()

def ChangeStatus(id_product:str):
  product= GetProductById(id_product)

  product.status = not product.status
  session.add(product) 
  session.commit()
  session.refresh(product)


  return product