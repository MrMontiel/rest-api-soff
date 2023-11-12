from enum import Enum
from pydantic import BaseModel
from typing import Optional



class UpdateUserBase(BaseModel):
    name : str
    document_type : str
    document : str
    phone : str
    email : str
    id_role: str
    

    
class UserBase(BaseModel):
    name : str
    document_type : str
    document : str
    phone : str
    email : str
    password : str
    id_role: str
    
    
        
class User(UserBase):
    id: Optional[str]
    status:bool = True
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserUpdate(UpdateUserBase):
    pass
