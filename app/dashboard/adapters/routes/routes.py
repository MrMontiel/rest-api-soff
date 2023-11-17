from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.adapters.services.user import getCurrentActivateUser
from app.auth.domain.pydantic.userauth import User
from app.dashboard.adapters.service.service import getTargetsDashboard, getGraficSales


dashboard = APIRouter(
  prefix='/dashboard',
  tags=["Dashboard"]
)

@dashboard.get('/')
async def get_targets():
  sales = getTargetsDashboard()
  return sales

@dashboard.get('/grafic_sales')
async def get_grafic():
  graficSales= getGraficSales()
  return graficSales