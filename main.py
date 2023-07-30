from fastapi import FastAPI
# Routes
from app.sales.routes.sales_router import sales

app = FastAPI()

# Add routes
app.include_router(sales)