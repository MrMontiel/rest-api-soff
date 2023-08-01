from app.providers.adapters.sqlachemy.provider import Provider

def ProviderSchema(provider: Provider) -> dict:
    return{
        "id": provider.id,
        "name": provider.name,
        "company": provider.price,
        "address": provider.quantity_stock,
        "date_registration": provider.unit_measure,
        "email": provider.email,
        "phone": provider.phone,
        "city": provider.city,
        "status": provider.status
    }
    
def providersSchema(providers: list [Provider]) -> list:
    return [ProviderSchema(provider)for provider in providers]
