import uuid
from sqlalchemy import select, delete, desc
from app.products.adapters.exceptions.exceptions import AmountSupplyMax, LowSalePrice, ProductNotFound, IdProductRequired, SupplyNotFound,ProductNotUpdate, DetailsRequired, InfoProductRequired, NameProductExist, DetailNotFound
from app.infrastructure.database import ConectDatabase, SessionLocal
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.products.adapters.serializers.product_schema import recipeDetailsSchema
from sqlalchemy.exc import PendingRollbackError

session = SessionLocal()

def format_price_and_subtotal(detail):
    detail.supply.price = round(detail.supply.price, 2)
    detail.subtotal = round(detail.subtotal, 2)
    return detail

def GetAllProducts(limit:int, offset:int, status:bool=True):
  try:
    products = session.scalars(select(Product).where(Product.status == status).offset(offset).limit(limit).order_by(desc(Product.register_date))).all()
    if not products:
      return []
    return products
  except PendingRollbackError as e:
    session.rollback()

def GetDetailsProduct(id_product:str):
  try:
    if not id_product:
      IdProductRequired()

    statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
    details = session.scalars(statement).all()
    return details
  except PendingRollbackError as e:
    session.rollback()

def GetProductById(id_product:str) ->Product:
  try:
    product = session.get(Product, id_product)
    if not product:
      ProductNotFound()
    return product
  except PendingRollbackError as e:
    session.rollback()

def CreateProduct ():
  try:
    products = session.scalars(select(Product)).all()
    for product in products:
      if product.name == "":
        id_product = product.id
        DeleteProduct(id_product)
        new_product = Product(name="", sale_price=0.0)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    new_product = Product(name="", sale_price=0.0)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
  except PendingRollbackError as e:
    session.rollback()

def AddDetail(id_product:str, detail: RecipeDetailCreate):
  try:
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
          if supply.unit_measure == "Gramos" and n.amount_supply < 20:
            AmountSupplyMax()
          session.add(n)
          session.commit()
          session.refresh(n) 
          return format_price_and_subtotal(n) 

      if supply.unit_measure == "Gramos" and detail.amount_supply < 20:
        AmountSupplyMax()

      new_detail = RecipeDetail(product_id=id_product, supply_id=detail.supply_id, amount_supply=detail.amount_supply, subtotal=total)
      session.add(new_detail)
      session.commit()
      session.refresh(new_detail)
      return format_price_and_subtotal(new_detail)

    ProductNotUpdate()
  except PendingRollbackError as e:
    session.rollback()

def ConfirmProduct(id_product:str, productCreate:ProductCreate): 
  try:
    product = GetProductById(id_product)

    if product.status:
      product_name = session.scalars(select(Product.name)).all()

      if not product:
        ProductNotFound()

      statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
      details = recipeDetailsSchema(session.scalars(statement).all())

      if len(details) <= 0:
        DetailsRequired()

      total:float = 0.0

      for detail in details:
        total += detail['subtotal']
      
      if productCreate.sale_price < total:
        LowSalePrice()

      product.name = productCreate.name
      product.price = total
      product.sale_price = productCreate.sale_price

      if productCreate.name in product_name:
        NameProductExist()

      if productCreate.name == "" or productCreate.sale_price == 0:
        InfoProductRequired()

      session.commit()
      session.refresh(product)
      return product
    
    ProductNotUpdate()
  except PendingRollbackError as e:
    session.rollback()

def UpdateDetail(id_detail:str, amount_supply:int):
    try:
      detail = session.get(RecipeDetail, uuid.UUID(id_detail))

      if not detail:
        DetailNotFound()

      if detail.supply.unit_measure == "Gramos" and amount_supply < 20:
        AmountSupplyMax()
        
      detail.amount_supply = amount_supply
      detail.subtotal = detail.supply.price * amount_supply
      session.add(detail)
      session.commit()
      session.refresh(detail)
      return format_price_and_subtotal(detail)
    except PendingRollbackError as e:
      session.rollback()

def UpdateProduct(id_product: str, productCreate:ProductCreate):
  try:
    product = GetProductById(id_product)

    if product.status:
      product_name = session.scalars(select(Product.name).where(Product.id != id_product)).all()

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

      if productCreate.sale_price < total:
          LowSalePrice()

      product.name = productCreate.name
      product.price = total
      product.sale_price = productCreate.sale_price

      # session.add(product)
      session.commit()
      session.refresh(product)
      return product
    ProductNotUpdate()
  except PendingRollbackError as e:
    session.rollback()

def DeleteDetail(id_detail:str):
  try:
    detail = session.get(RecipeDetail, uuid.UUID(id_detail))

    if not detail:
      DetailNotFound()

    session.delete(detail)  
    session.commit()
  except PendingRollbackError as e:
    session.rollback()

def DeleteProduct(id_product:str):
  try:
    product = session.get(Product, id_product)

    if not product:
      ProductNotFound()

    statement = select(RecipeDetail).where(RecipeDetail.product_id == id_product)
    details = recipeDetailsSchema(session.scalars(statement).all())
    
    if len(details) > 0:
      delete_statement = delete(RecipeDetail).where(RecipeDetail.product_id == id_product)
      session.execute(delete_statement)

    session.delete(product)
    session.commit()
  except PendingRollbackError as e:
    session.rollback()

def ChangeStatus(id_product:str):
  try:
    product= GetProductById(id_product)

    product.status = not product.status
    session.add(product) 
    session.commit()
    session.refresh(product)

    return product
  except PendingRollbackError as e:
    session.rollback()
