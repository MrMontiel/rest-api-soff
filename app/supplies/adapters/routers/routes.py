from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from app.supplies.adapters.serializers.supply_schema import SupplySchema
from fastapi import APIRouter, HTTPException, status
from app.supplies.adapters.services.services import GetAllSupplies, UpdateSupply, DeleteSupply
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.supplies.adapters.serializers.supply_schema import SupplySchema, suppliesSchema

from app.supplies.domain.pydantic.supply import SupplyCreate, SupplyUpdate, SupplyDelete

session = SessionLocal()

supplies = APIRouter(
    prefix='/supplies',
    tags=["Supplies"]
)

@supplies.get('/')
async def get_all_supplies(limit: int = 100):
    supplies = GetAllSupplies()
    return{
        "amount_supplies": len(supplies),
        "supplies": suppliesSchema(supplies)
    }

@supplies.post('/create_supply')
async def create_supply(supply: SupplyCreate):
  new_supply = Supply(name=supply.name, price=supply.price, quantity_stock=supply.quantity_stock, unit_measure=supply.unit_measure)
  session.add(new_supply)
  session.commit()
  session.refresh(new_supply)
  return {
    "Supply": SupplySchema(new_supply)
  }

    
@supplies.put('/update_supply/{id}')
async def update_supply_route(id: str, supply_update: SupplyUpdate):
    updated_supply = UpdateSupply(id, supply_update)
    if updated_supply:
        return {"supply": SupplySchema(updated_supply)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply not found")
    
    
@supplies.delete('/delete_supply/{id}')
async def delete_supply_route(id: str):
    delete_response = DeleteSupply(id)
    if delete_response:
        return {"message": "Supply deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_405_NOT_FOUND, detail="Supply not found")
      