from pydantic import BaseModel
from typing import Optional

class Credentials(BaseModel):
    username: str
    password: str

class User(BaseModel):
    # name: str | None = None
    name: Optional[str] = None
    email: str
    status: Optional[bool] = None
    # status: bool | None = None
    permissions: list[str]
    
class UserAuthenticated(User):
     # hashed_password: str | None = None
    hashed_password: Optional[str] = None
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
