from app.sales.sqlalchemy_models.sale_sqlalchemy import Product

def productSchema(product: Product) -> dict:
  return {
    "id": product.id,
    "name": product.name,
    "price": product.price
  }
  
def productsSchema(products: list[Product]) -> list:
  return [productSchema(product) for product in products]