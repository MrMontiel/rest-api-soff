from sqlalchemy import select
from app.infrastructure.database import ConectDatabase
from app.providers.adapters.serializers.provider_schema import providersSchema
from fastapi import APIRouter, HTTPException, status
from app.providers.adapters.services.services import GetAllProviders,AddProvider, UpdateProvider, DeleteProvider, GetOneProvider, UpdateStatusProvider
from app.providers.adapters.sqlachemy.provider import Provider
from app.providers.adapters.services.services import GetAllProviders
from app.providers.adapters.serializers.provider_schema import ProviderSchema, providersSchema
from app.providers.domain.pydantic.provider import ProviderCreate, ProviderUpdate, ProviderDelete



session = ConectDatabase.getInstance()

providers = APIRouter(
    prefix='/providers',
    tags=["Providers"]
)


@providers.get('/')
async def get_all_providers(limit: int = 100, offset: int = 0):
    providers = GetAllProviders(limit, offset)
    return{
        "amount_providers": len(providers),
        "providers": providersSchema(providers)
    }
    
@providers.get("/{id}/get_provider/")
async def get_provider(id: str ):
    providers = GetOneProvider(id)
    return{
        "supply":ProviderSchema(providers)
    }

    

@providers.post('/create_provider')
async def create_provider(provider: ProviderCreate):
  new_provider = AddProvider(provider)
  return {
    "Provider create": ProviderSchema(new_provider)
  }

  
@providers.put('/update_provider/{id}')
async def update_provider_route(id: str, provider_update: ProviderUpdate):
    updated_provider = UpdateProvider(id, provider_update)
    return {"Provider Update": ProviderSchema(updated_provider)
    }


@providers.delete('/delete_provider/{id}')
async def delete_provider_route(id: str):
    delete_provider = DeleteProvider(id)
    return{
        "Provider Delete": ProviderSchema(delete_provider)
        
    }
    
@providers.put("/{id}/status_update_provider")
async def updateStatusProvider(id:str):
    update_provider_route = UpdateStatusProvider(id)
    return{
        "Provider update": ProviderSchema(update_provider_route)
    }