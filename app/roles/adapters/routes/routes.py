from fastapi import APIRouter
from pydantic import BaseModel
from app.auth.adapters.services.user import User, getCurrentActivateUser
from fastapi import Depends
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
    updateStatusRole,
    updateRolesPermissions
)
from app.roles.domain.pydantic.role import AssignPermissions
from app.roles.adapters.serializer.roles_schema import (
    rolesSchema, 
    roleSchema, 
    permissionRolesSchema,
    permissionsRolesSchema
)

role = APIRouter(
    prefix= "/roles",
    tags=['Role']
)

#  ----------------------------------ROLE------------------------------------------
@role.get("/get-role")
async def get_role(limit: int =100, offset=0, status:bool=True, user: User = Depends(getCurrentActivateUser)):
    roles = get_roles(limit,offset,status)
    return rolesSchema(roles)

    
    
@role.get("/{id_role}/get_role_id/")
async def get_role_id(id_role: str, user: User = Depends(getCurrentActivateUser)):
    roles_get = get_id_role(id_role)
    return{
        "role":roleSchema(roles_get)
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
    
    
@role.post("/post-permissions/{nombre_role}")
async def assign_permissions(nombre_role:str, permissions: list[AssignPermissions] ):
    Permission_role_create(nombre_role, permissions)
    return {
        "message": "Permisos agregados"
    }
    
@role.put("/{id_role}/status-update-role")
async def updateStatusRol(id_role:str, user: User = Depends(getCurrentActivateUser)):
    updateStatusRole(id_role)
    return{
        "Mensaje": "update Status"
    }   
    

@role.get("/{id_permisssionrole}/permissionrole-get")
async def  get_permissionrole(id_permisssionrole:str):
    permissionrole_get_id= permissionroles_get(id_permisssionrole)
    return permissionsRolesSchema(permissionrole_get_id)

    
# ------------------------update roles permissions---
class UpdateRole(BaseModel):
    name: str
    permissions: list[AssignPermissions]
    
    
@role.put("/update_role/{id_rol}")
async def updaterolepermissions(id_rol:str, data: UpdateRole, user: User = Depends(getCurrentActivateUser)):
    roles_put = update_role(data.name, id_rol)
    update_permission_role= updateRolesPermissions(id_rol, data.permissions)
    
    return {
        "Permission_Role":"update Permissions"
    }
