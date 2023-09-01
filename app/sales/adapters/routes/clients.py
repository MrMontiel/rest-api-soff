from fastapi import APIRouter

clients = APIRouter(
  prefix="/clients",
  tags=["Clients"]
)

@clients.get('/')
async def get_all_clients():
  return {
    "message": "new Message"
  }