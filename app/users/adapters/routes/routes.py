from fastapi import APIRouter
from app.users.domain.pydantic.user import UserCreate
from app.users.adapters.services.services import (
    get_users,
    get_user_id,
    delete_user,
    post_user,
    user_update,
    )
from app.users.adapters.serializer.user_eschema import ( usersSchema,userSchema, )



user = APIRouter(
    prefix= "/user",
    tags=['User']
)



@user.get("/get-users")
async def get_user(limit: int =100):
    users = get_users()
    return{
        "user": len(users),
        "user": usersSchema(users)
    }
    

@user.post('/post_user')
async def get_id_user(user :UserCreate):
    user_new = post_user(user)
    return {
        "user": userSchema(user_new)  
    }
    
@user.get("/{id_user}/put-user")
async def update_user(id_user:str):
    id_user=get_user_id(id_user)
    return{
        "user": userSchema(id_user)
    }
    
    
@user.put("/{id_user}/put-user")
async def update_user(id_user:str, user: UserCreate):
    user_id_put= user_update(id_user,user)
    return{
        "user update": userSchema(user_id_put)
    }
    
@user.delete("/{id_user}/delete-user")
async def user_delete(id_user:str):
    del_user= delete_user(id_user)
    return{
        "Mensaje": "Deleted successfully"
    }   