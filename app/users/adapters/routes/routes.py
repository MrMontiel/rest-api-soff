from fastapi import APIRouter
from app.users.domain.pydantic.user import UserCreate, UserUpdate
from app.users.adapters.services.services import (
    get_users,
    get_user_id,
    delete_user,
    post_user,
    user_update,
    updateStatusUser
    )
from app.users.adapters.serializer.user_eschema import ( usersSchema,userSchema, )
from app.auth.adapters.services.user import User, getCurrentActivateUser
from fastapi import Depends

user = APIRouter(
    prefix= "/users",
    tags=['User']
)

@user.get("/")
async def get_user(limit: int =100 , offset=0, status:bool=True, user: User = Depends(getCurrentActivateUser)):
    users = get_users(limit,offset,status)
    return usersSchema(users)
    

@user.post('/')
async def get_id_user(users :UserCreate, user: User = Depends(getCurrentActivateUser)):
    user_new = post_user(users)
    return {
        "Create User": userSchema(user_new)  
    }
    
@user.get("/{id_user}")
async def get_user(id_user:str, user: User = Depends(getCurrentActivateUser)):
    id_user=get_user_id(id_user)
    return userSchema(id_user)
    
    
    
@user.put("/update_user/{id_user}")
async def update_user(id_user:str, users: UserUpdate, user: User = Depends(getCurrentActivateUser)):
    user_id_put= user_update(id_user,users)
    return {
            "Update user":userSchema(user_id_put)
        }
    
    
@user.delete("/delete_user/{id_user}")
async def user_delete(id_user:str, user: User = Depends(getCurrentActivateUser)):
    del_user= delete_user(id_user)
    return{
        "Delete User":userSchema(del_user)
    }   
    
    
@user.put("/status_update/{id_user}")
async def updateStatus(id_user:str, user: User = Depends(getCurrentActivateUser)):
    updateStatus_User=updateStatusUser(id_user)
    return{
        "Update Status User":userSchema(updateStatus_User)
    }   
    