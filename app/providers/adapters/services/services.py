import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.providers.domain.pydantic.provider import ProviderCreate, ProviderUpdate, ProviderDelete
from app.providers.adapters.sqlachemy.provider import Provider

session = ConectDatabase.getInstance()

def GetAllProviders(limit:int, offset: int):
  providers = session.scalars(select(Provider).where(Provider.status != False).offset(offset).limit(limit).order_by(desc(Provider.date_registration))).all()
  if not providers:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Providers not found")
  return providers


def GetOneProvider(id:str):
  providers = session.get(Provider, uuid.UUID(id))
  if not providers:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply not found")
  return providers

def AddProvider(provider: ProviderCreate):
  if not provider:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="provider not created")
  if provider.name == "" or provider.company == "" or provider.address == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the fields name, company, address and email: are obligatory")
  new_provider = Provider(name=provider.name, company=provider.company, address=provider.address, email=provider.email, phone=provider.phone, city=provider.city)
  
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="provider not found")
    
def DeleteProvider(id: str):
    provider = session.query(Provider).filter(Provider.id == uuid.UUID(id)).first()
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply not found")
    session.delete(provider)
    session.commit()
    return provider
  
def UpdateStatusProvider(id:str):
    provider = session.get(Provider, uuid.UUID(id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    provider.status= not provider.status
    session.add(provider)
    session.commit()
    return provider