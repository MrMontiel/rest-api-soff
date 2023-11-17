from sqlalchemy import select
from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException, status
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema,recipeDetailsSchema
from app.products.adapters.services.services import GetAllProducts, CreateProduct, AddDetail, ConfirmProduct, GetDetailsProduct, GetProductById, UpdateDetail, UpdateDetail, UpdateProduct, DeleteDetail, DeleteProduct, ChangeStatus
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.supplies.adapters.serializers.supply_schema import suppliesSchema
from app.auth.adapters.services.user import User, getCurrentActivateUser
from fastapi import Depends

session = ConectDatabase.getInstance()

products = APIRouter(
  prefix='/products',
  tags=["Products"]
)

@products.get('/')
async def get_all_products(limit: int = 100, offset:int =0, status:bool = True, user: User = Depends(getCurrentActivateUser)):
  products = GetAllProducts(limit, offset, status)
  return productsSchema(products)

@products.get('/{id_product}')
async def get_product_by_id(id_product: str, user: User = Depends(getCurrentActivateUser)):
  product = GetProductById(id_product)
  return productSchema(product)

@products.get('/{id_product}/details')
async def get_details_product(id_product: str, user: User = Depends(getCurrentActivateUser)):
  details = GetDetailsProduct(id_product)
  return  recipeDetailsSchema(details)

@products.post('/add_products')
async def create_product(user: User = Depends(getCurrentActivateUser)):
  new_product = CreateProduct()
  return {
    "id": new_product.id,
    "message": "product created successfully"
  }

@products.post('/{id_product}/add_detail')
async def add_detail(id_product:str, detail:RecipeDetailCreate, user: User = Depends(getCurrentActivateUser)):
  new_detail = AddDetail(id_product, detail)
  return {
    "id": new_detail.id,
    "message": "Detail added successfully"
  }

@products.put('/{id_product}/confirm_product')
async def confirm_product(id_product: str, productCreate: ProductCreate, user: User = Depends(getCurrentActivateUser)):
  product = ConfirmProduct(id_product, productCreate)
  return {
    "id_product": product.id,
    "product": productSchema(product)
  }

@products.put('/update_detail')
async def update_detail(id_detail:str, amount_supply: int, user: User = Depends(getCurrentActivateUser)):
  detail = UpdateDetail(id_detail, amount_supply)
  return recipeDetailSchema(detail)

@products.put('/{id_product}/update_product')
async def update_product(id_product:str, products:ProductCreate, user: User = Depends(getCurrentActivateUser)):
  product = UpdateProduct(id_product, products)
  return productSchema(product)

@products.delete('/{id_detail}/delete_detail')
async def delete_detail(id_detail:str, user: User = Depends(getCurrentActivateUser)):
  DeleteDetail(id_detail)
  return {
    "message":"Detail deleted successfully"
  }

@products.delete('/{id_product}/delete_product')
async def delete_product(id_product:str, user: User = Depends(getCurrentActivateUser)):
  DeleteProduct(id_product)
  return {
    "message":"Product deleted successfully"
  }

@products.put('/{id_product}/change_status')
async def change_status(id_product:str, user: User = Depends(getCurrentActivateUser)):
  ChangeStatus(id_product)
  return{
    "message":"Status updated"
  }