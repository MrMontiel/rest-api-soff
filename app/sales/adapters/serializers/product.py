from app.sales.adapters.sqlalchemy.sale import Product

def productSchema(product: Product) -> dict:
  return {
    "id": product.id,
    "name": product.name,
    "price": product.price
  }
  
def productsSchema(products: list[Product]) -> list:
  return [productSchema(product) for product in products]