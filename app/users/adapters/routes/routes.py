from fastapi import APIRouter
from app.users.domain.pydantic.user import UserCreate, RoleCreate, PermissionCreate, PermissionsRolesCreate
from app.users.adapters.services.services import (
    create_permission,
    get_id_permission,
    get_permission,
    update_permission,
    delete_permission,
    get_roles, 
    get_id_role, 
    create_rol, 
    update_role,
    get_users,
    get_user_id,
    delete_user,
    post_user,
    user_update,
    delete_role_service,
    permissionsrole_create,
    permissionroles_get,
    replace_role_base
    )
from app.users.adapters.serializer.user_eschema import (
    PermissionsSchema,
    permissionSchema, 
    usersSchema,userSchema, 
    rolesSchema, roleSchema, 
    permissionRolesSchema,
    permissionsRolesSchema
    )



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
# ----------------------------------PERMISSION------------------------------------------

@user.post("/post-permision")
async def post_permission(permission: PermissionCreate):
    permission = create_permission(permission)
    return{
        "id": permission.id,
        "name": permission.name
    }


@user.get("/get-permision")
async def get_permissions(limit:int= 10):
    permissions_get = get_permission()
    return{
        "Permissions": PermissionsSchema(permissions_get)
    }
@user.get("/{id_permission}/get_permission_id")
async def get_permissinon_id(id_permission : str):
    permission = get_id_permission(id_permission)
    return{
        "permission": permissionSchema(permission)
    }
    
@user.put("/{id_permission}/put_permission")
async def put_permission(id_permission : str, permission: PermissionCreate): 
    permission_get = update_permission(id_permission, permission)
    return{
        "permission": permissionSchema(permission_get),
        "mensaje": "Update Permission"
    }
@user.delete("/{id_permission}/delete-permission")
async def permission_delete(id_permission:str):
    permissio_delete_id= delete_permission(id_permission)
    return{
        "Permission delete:": permissionSchema(permissio_delete_id)
    }
# ----------------------------------ROLE------------------------------------------
@user.get("/get-role")
async def get_role(limit: int =10):
    roles = get_roles()
    return{
        "amount_roles": len(roles),
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
    
# ----------------------------------ROLEPERMISSION----------------------------------------------
@user.post("/post-permissinosrole")
async def create_permissionsrole(permissionsrole :PermissionsRolesCreate):
    new_permissionrole= permissionsrole_create(permissionsrole)
    return{
        "Permission_Role": permissionRolesSchema(new_permissionrole)
    }
    
@user.get("/{id_permissionrole}/permissionrole-get")
async def  get_permissionrole(id_permisssionrole:str):
    permissionrole_get_id= permissionroles_get(id_permisssionrole)
    return{
        "Permision Role": permissionsRolesSchema(permissionrole_get_id)
    }
    
# ----------------------------------TESTING----------------------------------------------
@user.get("/{id_role}/testin-replece")
async def replace_testin(id_role:str):
    replace_role=replace_role_base(id_role)
    return{
        "role Replace": usersSchema(replace_role)
    }
    