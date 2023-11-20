import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.providers.domain.pydantic.provider import ProviderCreate, ProviderUpdate, ProviderDelete
from app.providers.adapters.sqlachemy.provider import Provider
from app.purchases.adapters.serializers.purchase_schema import purchasesSchema
from app.purchases.adapters.sqlalchemy.purchase import Purchase
from app.providers.adapters.exceptions.exceptions import (
  noprovider,
  requiredprovider,
  notcreatedprovider,
  notdeleteprovider,
  notupdateprovider,
  nitisalreadyexist,
  providerassociated
)
from sqlalchemy.exc import PendingRollbackError
# from app.providers.adapters.exceptions import noprovider, requiredprovider

session = ConectDatabase.getInstance()

def GetAllProviders(limit:int, offset: int, status:bool=True):
  try:
    providers = session.scalars(select(Provider).where(Provider.status == status).offset(offset).limit(limit).order_by(desc(Provider.date_registration))).all()
    if not providers:
        []
    return providers
  except PendingRollbackError as e:
        session.rollback()


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
    
  try:
    provider_nit = session.scalars(select(Provider.nit)).all()
    if provider.nit in provider_nit:
      nitisalreadyexist()
  
    
    new_provider = Provider(nit=provider.nit, name=provider.name, company=provider.company, address=provider.address, phone=provider.phone, city=provider.city)
  
    session.add(new_provider)
    session.commit()
    session.refresh(new_provider)
    return new_provider
  except PendingRollbackError as e:
        session.rollback()
    
def UpdateProvider(id: str, provider_update: ProviderUpdate):
  try:
    provider_id_update = GetOneProvider(id)
    if not provider_id_update:
        requiredprovider()

    existing_provider = session.query(Provider).filter(
        Provider.nit == provider_update.nit, Provider.id != id).first()
    
    if existing_provider:
        nitisalreadyexist()

    provider_id_update.nit = provider_update.nit
    provider_id_update.name = provider_update.name
    provider_id_update.company = provider_update.company
    provider_id_update.address = provider_update.address
    provider_id_update.phone = provider_update.phone
    provider_id_update.city = provider_update.city
    session.commit()
    session.refresh(provider_id_update)
    return provider_id_update
  except PendingRollbackError as e:
        session.rollback()
      

    
def DeleteProvider(id: str):
  try:
    provider = session.query(Provider).filter(Provider.id == uuid.UUID(id)).first()
    
    statement = select(Purchase).where(Purchase.provider_id == id)
    details = purchasesSchema(session.scalars(statement).all())
    if details:
      providerassociated()
      
    if not provider:
      notdeleteprovider()
    session.delete(provider)
    session.commit()
    return provider
  except PendingRollbackError as e:
      session.rollback()
  
def UpdateStatusProvider(id:str):
  try:
    provider = session.get(Provider, uuid.UUID(id))
    if not provider:
        notupdateprovider()
    provider.status= not provider.status
    session.add(provider)
    session.commit()
    return provider
  except PendingRollbackError as e:
      session.rollback()