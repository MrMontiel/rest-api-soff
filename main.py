from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Routes
from app.purchases.adapters.routes.purchases import purchases
from app.supplies.adapters.routers.routes import supplies
from app.providers.adapters.routers.routes import providers
from app.sales.adapters.routes.sales import sales
from app.products.adapters.routes.routes import products
from app.sales.adapters.routes.sales import sales
from app.users.adapters.routes.routes import user
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes

app.include_router(purchases)
app.include_router(sales)
app.include_router(supplies)
app.include_router(providers)
app.include_router(products)
app.include_router(user)