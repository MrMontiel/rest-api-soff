from app.providers.adapters.sqlachemy.provider import Provider

def ProviderSchema(provider: Provider) -> dict:
    return{
        "id": provider.id,
        "nit": provider.nit,
        "name": provider.name,
        "company": provider.company,
        "address": provider.address,
        "date_registration": provider.date_registration,
        # "email": provider.email,
        "phone": provider.phone,
        "city": provider.city,
        "status": provider.status
    }
    
def providersSchema(providers: list [Provider]) -> list:
    return [ProviderSchema(provider)for provider in providers]
