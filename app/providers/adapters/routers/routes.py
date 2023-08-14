from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from app.providers.adapters.serializers.provider_schema import providersSchema
from fastapi import APIRouter, HTTPException, status
from app.providers.adapters.services.services import GetAllProviders, UpdateProvider, DeleteProvider
from app.providers.adapters.sqlachemy.provider import Provider
from app.providers.adapters.services.services import GetAllProviders
from app.providers.adapters.serializers.provider_schema import ProviderSchema, providersSchema
from app.providers.domain.pydantic.provider import ProviderCreate, ProviderUpdate, ProviderDelete



session = SessionLocal()

providers = APIRouter(
    prefix='/providers',
    tags=["Providers"]
)


@providers.get('/')
async def get_all_providers(limit: int = 100):
    providers = GetAllProviders()
    return{
        "amount_providers": len(providers),
        "providers": providersSchema(providers)
    }
    

@providers.post('/create_provider')
async def create_provider(provider: ProviderCreate):
  new_provider = provider(name=provider.name, company=provider.company, address=provider.address, date_registration=provider.date_registration, email=provider.email, phone=provider.phone, city=provider.city)
  session.add(new_provider)
  session.commit()
  session.refresh(new_provider)
  return {
    "Provider": providersSchema(new_provider)
  }

  
@providers.put('/update_provider/{id}')
async def update_provider_route(id: str, provider_update: ProviderUpdate):
    updated_provider = UpdateProvider(id, provider_update)
    if updated_provider:
        return {"provider": providersSchema(updated_provider)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="provider not found")


@providers.delete('/delete_provider/{id}')
async def delete_provider_route(id: str):
    delete_response = DeleteProvider(id)
    if delete_response:
        return {"message": "Provider deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_405_NOT_FOUND, detail="SProvider not found")
      