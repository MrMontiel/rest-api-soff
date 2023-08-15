from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from app.supplies.adapters.serializers.supply_schema import SupplySchema
from fastapi import APIRouter, HTTPException, status
from app.supplies.adapters.services.services import GetAllSupplies, UpdateSupply, DeleteSupply, AddSupply, GetOneSupply
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

@supplies.get("/{id}/get_supply/")
async def get_supply(id: str ):
    supplies = GetOneSupply(id)
    return{
        "supply":SupplySchema(supplies)
    }




@supplies.post('/create_supply')
async def create_supply(supply: SupplyCreate):
    new_supply = AddSupply(supply)
    return {
    "Supply Create": SupplySchema(new_supply)
    }

    
@supplies.put('/update_supply/{id}')
async def update_supply_route(id: str, supply_update: SupplyUpdate):
    updated_supply = UpdateSupply(id, supply_update)
    return {"Supply Update": SupplySchema(updated_supply)
    }
    
    
@supplies.delete('/delete_supply/{id}')
async def delete_supply_route(id: str):
    delete_supply = DeleteSupply(id)
    return{
        "Supply Delete": SupplySchema(delete_supply)
        
    }