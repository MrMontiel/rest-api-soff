from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.adapters.services.user import getCurrentActivateUser
from app.auth.domain.pydantic.userauth import User
from app.dashboard.adapters.service.service import getPyment,getTargetsDashboard, getGraficSales, get_topproducts
from app.auth.domain.pydantic.userauth import User

dashboard = APIRouter(
  prefix='/dashboard',
  tags=["Dashboard"]
)

@dashboard.get('/')
async def get_targets(user: User = Depends(getCurrentActivateUser)):
  sales = getTargetsDashboard()
  return sales

@dashboard.get('/grafic_sales')
async def get_grafic(user: User = Depends(getCurrentActivateUser)):
  graficSales= getGraficSales()
  return graficSales

@dashboard.get('/grafic_payment')
async def get_grafic_payment(user: User = Depends(getCurrentActivateUser)):
  graficpaymnet= getPyment()
  return graficpaymnet

@dashboard.get('/grafic_payment2')
async def get_top_products(user: User = Depends(getCurrentActivateUser)):
  top_products = get_topproducts()
  return top_products