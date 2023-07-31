from fastapi import FastAPI
# Routes
from app.sales.adapters.routes.routes import sales

app = FastAPI()

# Add routes
app.include_router(sales)