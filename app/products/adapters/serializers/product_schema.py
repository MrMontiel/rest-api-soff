from app.products.adapters.sqlalchemy.product import Product, RecipeDetail

def productSchema(product:Product)-> dict:
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "sale_price": product.sale_price,
        "status":product.status
    }

def productsSchema(products:list[Product])->list:
    return [productSchema(product) for product in products]

def recipeDetailSchema(recipeDetail:RecipeDetail)-> dict:
    return {
        "product_id": recipeDetail.product_id,
        "supply_id": recipeDetail.supply_id,
        "supply": recipeDetail.supply,
        "amount_supply": recipeDetail.amount_supply,
        "unit_measure": recipeDetail.unit_measure,
        "subtotal":recipeDetail.subtotal
    }

def recipeDetailsSchema(recipeDetails:list[RecipeDetail])->list:
    return [recipeDetailSchema(recipe) for recipe in recipeDetails]
