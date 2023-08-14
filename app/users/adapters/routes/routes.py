from fastapi import APIRouter
import uuid 
# from app.users.adapters.services.services import get_users, post_user, create_rol, get_roles, get_id_role, update_role
from app.users.adapters.services.services import (
    get_roles, 
    get_id_role, 
    create_rol, 
    update_role,
    get_users,
    post_user,
    delete_role_service,
    
    )
from app.users.adapters.serializer.user_eschema import usersSchema, rolesSchema, roleSchema
from app.users.domain.pydantic.user import UserCreate, RoleCreate, PermissionCreate



user = APIRouter(
    prefix= "/user",
    tags=['User']
)



@user.get("/get-user")
async def get_user(limit: int =100):
    users = get_users()
    return{
        "amount_users": len(users),
        "user": usersSchema(users)
    }
    

@user.post('/post_user')
async def create_user(user :UserCreate):
    new_user = post_user(user)
    return {
        # "id" : new_user.id
        "user": usersSchema(new_user)  
    }


# ----------------------------------ROLE------------------------------------------
@user.get("/get-role")
async def get_role(limit: int =10):
    roles = get_roles()
    return{
        "amount_users": len(roles),
        "user": rolesSchema(roles)
    }
    
@user.post("/post_rol")
async def post_rol(role : RoleCreate):
    new_role = create_rol(role)
    return{
        "id" : new_role.id,
        "name": new_role.name,
        "message": "Rol created successfully"
        
    }
    
    
@user.get("/{id_role}/get_role_id/")
async def get_role_id(id_role: str ):
    roles_get = get_id_role(id_role)
    return{
        "role":roleSchema(roles_get)
    }



    
@user.put("/{id_role}/put-role")
async def put_rol(id_role:str, role : RoleCreate):
    roles_put = update_role(role, id_role)
    return{
        "role": roleSchema(roles_put),
    }
    
    
@user.delete("/{id_role}/delete-role")
async def delete_role(id_role : str):
    rol_delete = delete_role_service(id_role)
    return{
        "role_Delete": roleSchema(rol_delete)
        
    }