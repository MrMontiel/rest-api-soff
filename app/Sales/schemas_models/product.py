from app.Sales.sqlalchemy_models.sale import ProductFail

def productSchema(product: ProductFail) -> dict:
  return {
    "id": product.id,
    "name": product.name,
    "price": product.price
  }
  
def productsSchema(products: list[ProductFail]) -> list:
  return [productSchema(product) for product in products]