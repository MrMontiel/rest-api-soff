import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.providers.domain.pydantic.provider import ProviderCreate, ProviderUpdate, ProviderDelete
from app.providers.adapters.sqlachemy.provider import Provider
from app.providers.adapters.exceptions.exceptions import (
  noprovider,
  requiredprovider,
  notcreatedprovider,
  notdeleteprovider,
  notupdateprovider,
  nameisalreadyexist
)
# from app.providers.adapters.exceptions import noprovider, requiredprovider

session = ConectDatabase.getInstance()

def GetAllProviders(limit:int, offset: int):
  providers = session.scalars(select(Provider).offset(offset).limit(limit).order_by(desc(Provider.date_registration))).all()
  if not providers:
    noprovider()
  return providers


def GetOneProvider(id:str):
  providers = session.get(Provider, uuid.UUID(id))
  if not providers:
    noprovider()
  return providers

def AddProvider(provider: ProviderCreate):
  if not provider:
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="provider not created")
    notcreatedprovider()
  if provider.nit == "" or provider.name == "" or provider.company == "" or provider.address == "" or provider.phone == "" or provider.city == "":
    requiredprovider()
    
  existing_provider = session.query(Provider).filter(Provider.nit == provider.nit).first()
  if provider.nit == existing_provider:
    nameisalreadyexist()
    
  else:
    new_provider = Provider(nit=provider.nit, name=provider.name, company=provider.company, address=provider.address, phone=provider.phone, city=provider.city)
  
    session.add(new_provider)
    session.commit()
    session.refresh(new_provider)
    return new_provider
    
def UpdateProvider(id: str, provider_update: ProviderUpdate):
    provider = session.get(Provider, uuid.UUID(id))
    print(provider)
    # provider = session.query(Provider).filter(Provider.id == uuid.UUID(id)).first()
    
    if provider:
        for attr, value in provider_update.dict().items():
            setattr(provider, attr, value)
        session.commit()
        session.refresh(provider)
        return provider
    else:
        notupdateprovider()
    
def DeleteProvider(id: str):
    provider = session.query(Provider).filter(Provider.id == uuid.UUID(id)).first()
    if not provider:
        notdeleteprovider()
    session.delete(provider)
    session.commit()
    return provider
  
def UpdateStatusProvider(id:str):
    provider = session.get(Provider, uuid.UUID(id))
    if not provider:
        notupdateprovider()
    provider.status= not provider.status
    session.add(provider)
    session.commit()
    return provider