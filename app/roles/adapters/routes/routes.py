from fastapi import APIRouter

from app.roles.domain.pydantic.role import RoleCreate, PermissionsRolesCreate
from app.roles.adapters.services.services import (
    get_roles, 
    get_id_role, 
    create_rol, 
    update_role,
    delete_role_service,
    replace_role_base,
    permissionsrole_create,
    permissionroles_get,
    Permission_role_create,
    updateStatusRole
)
from app.roles.domain.pydantic.role import AssignPermissions
from app.roles.adapters.serializer.roles_schema import (
    rolesSchema, 
    roleSchema, 
    permissionRolesSchema,
    permissionsRolesSchema
)

role = APIRouter(
    prefix= "/role",
    tags=['Role']
)

#  ----------------------------------ROLE------------------------------------------
@role.get("/get-role")
async def get_role(limit: int =10):
    roles = get_roles()
    return{
        "role": rolesSchema(roles)
    }
    
@role.post("/post_rol")
async def post_rol(role : RoleCreate):
    new_role = create_rol(role)
    return{
        "role":roleSchema(new_role)
    }
    
    
@role.get("/{id_role}/get_role_id/")
async def get_role_id(id_role: str ):
    roles_get = get_id_role(id_role)
    return{
        "role":roleSchema(roles_get)
    }



    
@role.put("/{id_role}/put-role")
async def put_rol(id_role:str, role : RoleCreate):
    roles_put = update_role(role, id_role)
    return{
        "role": roleSchema(roles_put),
    }
    
    
@role.delete("/{id_role}/delete-role")
async def delete_role(id_role : str):
    rol_delete = delete_role_service(id_role)
    return{
        "role_Delete": roleSchema(rol_delete) 
        # "role_Delete": "role delete " 
        
    }
    

    
    
    
# ----------------------------------ROLEPERMISSION----------------------------------------------
@role.post("/post-permissinosrole")
async def create_permissionsrole(permissionsrole :PermissionsRolesCreate):
    new_permissionrole= permissionsrole_create(permissionsrole)
    print(new_permissionrole)
    return{
        "Permission_Role": permissionRolesSchema(new_permissionrole)
    }
    
@role.get("/{id_permisssionrole}/permissionrole-get")
async def  get_permissionrole(id_permisssionrole:str):
    permissionrole_get_id= permissionroles_get(id_permisssionrole)
    return {
        "Permission_Role":permissionsRolesSchema(permissionrole_get_id)
        
        }
    
    
    
    
    
@role.post("/post-permissions/{nombre_role}")
async def assign_permissions(nombre_role:str, permissions: list[AssignPermissions]):
    Permission_role_create(nombre_role, permissions)
    return {
        "message": "Permisos agregados"
    }
    
@role.put("/{id_role}/status-update-role")
async def updateStatusRol(id_role:str):
    updateStatusRole(id_role)
    return{
        "Mensaje": "update Status"
    }   
    