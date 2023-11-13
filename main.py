from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Routes
from app.sales.adapters.routes.sales import sales
from app.supplies.adapters.routes.routes import supplies
from app.providers.adapters.routes.routes import providers
from app.purchases.adapters.routes.purchases import purchases
from app.products.adapters.routes.routes import products
from app.users.adapters.routes.routes import user
from app.roles.adapters.routes.routes import role
from app.permissions.adapters.routes.routes import permission
from app.dashboard.adapters.routes.routes import dashboard
from app.auth.adapters.routes.routes import auth



app = FastAPI()

origins = [
    "https://frontend-soff.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Add routes
app.include_router(auth)
app.include_router(dashboard)
app.include_router(purchases)
app.include_router(sales)
app.include_router(supplies)
app.include_router(providers)
app.include_router(products)
app.include_router(user)
app.include_router(role)
app.include_router(permission)

