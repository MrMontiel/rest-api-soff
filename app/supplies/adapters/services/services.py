import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.supplies.domain.pydantic.supply import SupplyCreate, SupplyUpdate, SupplyDelete
from app.supplies.adapters.sqlalchemy.supply import Supply

session = SessionLocal()



def GetAllSupplies(limit:int = 100):
  supplies = session.scalars(select(Supply)).all()
  if not supplies:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="supplies not found")
  return supplies


def AddSupply(supply: SupplyCreate):
  if not supply:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="supply not created")
  else: 
    new_supply = supply(name=supply.name, price=supply.price, quantity_stock=supply.quantity_stock, unit_measure=supply.unit_measure)
    session.add(new_supply)
    session.commit()
    session.refresh(supply)
    
    
def UpdateSupply(id: str, supply_update: SupplyUpdate):
    supply = session.query(Supply).filter(Supply.id == uuid.UUID(id)).first()
    if supply:
        for attr, value in supply_update.dict().items():
            setattr(supply, attr, value)
        session.commit()
        session.refresh(supply)
        return supply
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply not found")
      
      
def DeleteSupply(id: str):
    supply = session.query(Supply).filter(Supply.id == uuid.UUID(id)).first()
    if supply:
        session.delete(supply)
        session.commit()
        return True
    else:
        return False







# def UpdateSupply(supply: SupplyUpdate):
#   if not supply:
#     raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="supply not Updated")


# def DeleteSupply(supply: SupplyDelete):
#   if not supply:
#     raise HTTPException(status_code=status.HTTP_402_BAD_REQUEST, detail="supply not Delete")

def ConfirmSupply():
  pass


def ChangeState():
  pass