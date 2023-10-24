from pydantic import BaseModel
from typing import Optional

class ProviderBase(BaseModel):
    nit: str
    name: str
    company: str
    address: str
    # email: str
    phone: str
    city: str
    
class Provider(ProviderBase):
    id: Optional[str]
    date_registration: Optional[str]
    status: bool = True
    
    class Config:
        from_attributes = True
    
class ProviderCreate(ProviderBase):
    
    pass

class ProviderUpdate(ProviderBase):
    
    pass

class ProviderDelete(ProviderBase):
    
    pass