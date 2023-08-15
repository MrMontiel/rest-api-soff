from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException, status
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema,recipeDetailsSchema
from app.products.adapters.services.services import GetAllProducts, CreateProduct, AddDetail, ConfirmProduct, GetDetailsProduct, GetProductById, UpdateDetail
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate, ProductBase

session = ConectDatabase.getInstance()

products = APIRouter(
  prefix='/products',
  tags=["Products"]
)

@products.get('/')
async def get_all_products(limit: int = 100):
  products = GetAllProducts()
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
async def create_product(product: ProductCreate):
  new_product = CreateProduct(product)
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

@products.put('/{id_product}/{id_supply}/update_detail')
async def update_detail(id_product: str, id_supply:str, recipeDetailCreate: RecipeDetailCreate):
  UpdateDetail(id_product, id_supply, recipeDetailCreate)
  return{
    "message": "Detail updated successfully"
  }


