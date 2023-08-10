from fastapi import FastAPI
# Routes
from app.sales.adapters.routes.routes import sales
from app.supplies.adapters.routers.routes import supplies
from app.providers.adapters.routers.routes import providers

app = FastAPI()

# Add routes
app.include_router(sales)

app.include_router(supplies)


app.include_router(providers)