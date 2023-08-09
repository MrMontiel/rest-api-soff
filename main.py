from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Routes
from app.sales.adapters.routes.sales import sales

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
app.include_router(sales)