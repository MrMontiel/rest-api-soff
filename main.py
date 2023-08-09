from fastapi import FastAPI
# Routes
from app.sales.adapters.routes.routes import sales
from app.products.adapters.routes.routes import products

app = FastAPI()

# Add routes
app.include_router(sales)
app.include_router(products)