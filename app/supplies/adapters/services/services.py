import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.supplies.domain.pydantic.supply import SupplyCreate, SupplyUpdate, SupplyDelete
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.supplies.adapters.exceptions.exceptions import (
  notsupply,
  requiredsupply,
  notcreatedsupply,
  notdeletesupply,
  notupdatesupply,
  nameisalreadyexist
)

session = ConectDatabase.getInstance()



def GetAllSupplies(limit:int, offset: int):
  supplies = session.scalars(select(Supply).offset(offset).limit(limit).order_by(desc(Supply.name))).all()
  if not supplies:
    notsupply()
  return supplies


def GetOneSupply(id:str):
  supplies = session.get(Supply, id)
  if not supplies:
    notsupply()
  return supplies


def AddSupply(supply: SupplyCreate):
  if not supply:
    notcreatedsupply()
    
  existing_supply = session.query(Supply).filter(Supply.name == supply.name).first()
    # supply_name = session.scalars(select(supply.name)).all()
  if supply.name == existing_supply:
    nameisalreadyexist() 

  if supply.unit_measure == "Kilogramos":
    supply.unit_measure = "Gramos"
    
  if supply.name == "" or supply.price == "" or supply.quantity_stock == "" or supply.unit_measure == "":
    requiredsupply() 
    
  else:
    new_supply = Supply(name=supply.name, price=supply.price, quantity_stock=supply.quantity_stock, unit_measure=supply.unit_measure)
    
    session.add(new_supply)
    session.commit()
    session.refresh(new_supply)
    return new_supply
    
    
def UpdateSupply(id: str, supply_update: SupplyUpdate):
    supply = session.query(Supply).filter(Supply.id == uuid.UUID(id)).first()
    if supply:
        for attr, value in supply_update.dict().items():
            setattr(supply, attr, value)
        session.commit()
        session.refresh(supply)
        return supply
    else:
      notupdatesupply()
      
      
def DeleteSupply(id: str):
    supply = session.query(Supply).filter(Supply.id == uuid.UUID(id)).first()
    if not supply:
      notdeletesupply()
    session.delete(supply)
    session.commit()
    return supply


def UpdateStatusSupply(id:str):
    supply = session.get(Supply, uuid.UUID(id))
    if not supply:
      notupdatesupply()
    supply.status= not supply.status
    session.add(supply)
    session.commit()
    return supply






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