from fastapi import FastAPI
# Routes
from app.Sales.routes.sales_router import sales

app = FastAPI()

# Add routes
app.include_router(sales)