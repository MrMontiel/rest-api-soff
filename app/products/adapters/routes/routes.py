from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException, status
from app.products.adapters.serializers.product_schema import (
  productSchema,
  productsSchema,
  recipeDetailSchema,
  recipeDetailsSchema
)
from app.products.adapters.services.services import (
  GetAllProducts,
  CreateProduct,
  AddDetail,
  ConfirmProduct,
  GetDetailsProduct,
  GetProductById,
  UpdateDetail,
  UpdateDetail,
  UpdateProduct,
  DeleteDetail,
  ChangeStatus
)
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase

session = ConectDatabase.getInstance()

products = APIRouter(
  prefix='/products',
  tags=["Products"]
)

@products.get('/')
<<<<<<< HEAD
async def get_all_products(limit: int = 10, skip: int = 0):
  products = GetAllProducts(limit, skip)
=======
async def get_all_products(limit: int = 10, offset:int =0):
  products = GetAllProducts(limit, offset)
>>>>>>> 2eb1d5a7faa9d3656d80c9da5d1b535cb80a0a8d
  return {
    "amount_products": len(products),
    "products": productsSchema(products)
  }

@products.get('/{id_product}')
async def get_product_by_id(id_product: str):
  product = GetProductById(id_product)
  return {
    "product": productSchema(product)
  }

@products.get('/{id_product}/details')
async def get_details_product(id_product: str):
  details = GetDetailsProduct(id_product)
  return {
    "id_product": id_product,
    "details": recipeDetailsSchema(details)
  }

@products.post('/add_products')
async def create_product():
  new_product = CreateProduct()
  return {
    "id": new_product.id,
    "message": "product created successfully"
  }

@products.post('/{id_product}/add_detail')
async def add_detail(id_product:str, detail:RecipeDetailCreate):
  new_detail = AddDetail(id_product, detail)
  return {
    "id": new_detail.id,
    "message": "Detail added successfully"
  }

@products.put('/{id_product}/confirm_product')
async def confirm_product(id_product: str, productCreate: ProductCreate):
  product = ConfirmProduct(id_product, productCreate)
  return {
    "id_product": product.id,
    "product": productSchema(product)
  }

@products.put('/update_detail')
async def update_detail(id_detail:str, amount_supply: int):
  detail = UpdateDetail(id_detail, amount_supply)
  return recipeDetailSchema(detail)

@products.put('/update_product')
async def update_product(id_product:str, products:ProductCreate):
  product = UpdateProduct(id_product, products)
  return productSchema(product)

@products.delete('/{id_detail}/delete_detail')
async def delete_detail(id_detail:str):
  DeleteDetail(id_detail)
  return {
    "message":"Detail deleted successfully"
  }

@products.put('/{id_product}/change_status')
async def change_status(id_producto:str):
  ChangeStatus(id_producto)
  return{
    "message":"Status updated"
  }