from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.adapters.services.user import getCurrentActivateUser
from app.auth.domain.pydantic.userauth import User
from app.dashboard.adapters.service.service import getTargetsDashboard


dashboard = APIRouter(
  prefix='/dashboard',
  tags=["Dashboard"]
)

@dashboard.get('/')
async def get_targets( user: User = Depends(getCurrentActivateUser)):
  if "dashboard" in user.permissions:
    sales = getTargetsDashboard()
    return sales
  else:
    raise HTTPException(status_code=401, detail="No tienes acceso a este parte.")