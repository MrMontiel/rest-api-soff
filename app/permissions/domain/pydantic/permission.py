from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    name : str
       
class Permission(PermissionBase):
    id: Optional[str]
    class Config:
        from_attributes = True

class PermissionCreate(PermissionBase):
    pass