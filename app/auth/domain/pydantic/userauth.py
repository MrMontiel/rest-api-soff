from pydantic import BaseModel

class Credentials(BaseModel):
    username: str
    password: str

class User(BaseModel):
    name: str | None = None
    email: str
    status: bool | None = None
    permissions: list[str]
    
class UserAuthenticated(User):
     hashed_password: str | None = None
    
class TokenResponse():
    access_token: str
    refresh_token: str
