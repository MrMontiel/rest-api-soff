from app.infrastructure.database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from app.products.adapters.serializers.product_schema import productSchema, productsSchema, recipeDetailSchema,recipeDetailsSchema
from app.products.adapters.services.services import GetAllProducts, CreateProduct, AddDetail, ConfirmProduct, GetAllDetails
from app.products.domain.pydantic.product import ProductCreate, RecipeDetailCreate

session = SessionLocal()

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

@products.get('/details')
async def get_all_details(limit: int = 100):
  details = GetAllDetails()
  return {
    "amount_details": len(details),
    "details": recipeDetailsSchema(details)
  }

@products.post('/')
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
    "product_id": new_detail.product_id,
    "supply_is": new_detail.supply_id,
    "message": "Detail added successfully"
  }

@products.put('/{id_product}/confirm_product')
async def confirm_product(id_product: str, productCreate: ProductCreate):
  product = ConfirmProduct(id_product, productCreate)
  return {
    "id_product": product.id,
    "producto": productSchema(product)
  }

