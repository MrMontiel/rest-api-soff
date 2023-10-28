from fastapi import APIRouter, HTTPException, status
from app.dashboard.adapters.service.service import getTargetsDashboard

dashboard = APIRouter(
  prefix='/dashboard',
  tags=["Dashboard"]
)

@dashboard.get('/')
async def get_targets():
    sales = getTargetsDashboard()
    return sales