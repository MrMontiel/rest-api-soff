from fastapi import APIRouter
from app.permissions.domain.pydantic.permission import PermissionCreate
from app.permissions.adapters.services.services import (
    create_permission,
    get_id_permission,
    get_permission,
    update_permission,
    delete_permission
)

from app.permissions.adapters.serializer.roles_schema import (
    PermissionsSchema,
    permissionSchema
    )

from app.auth.adapters.services.user import User, getCurrentActivateUser
from fastapi import Depends


permission = APIRouter(
    prefix= "/permissions",
    tags=['permissions']
)
# ----------------------------------PERMISSION------------------------------------------

@permission.post("/post-permision")
async def post_permission(permission: PermissionCreate):
    permission = create_permission(permission)
    return permissionSchema(permission)



@permission.get("/get-permision")
async def get_permissions(limit:int= 10):
    permissions_get = get_permission()
    return PermissionsSchema(permissions_get)

@permission.get("/{id_permission}/get_permission_id")
async def get_permissinon_id(id_permission : str, user: User = Depends(getCurrentActivateUser)):
    permission = get_id_permission(id_permission)
    return  permissionSchema(permission)
        
    
@permission.put("/{id_permission}/put_permission")
async def put_permission(id_permission : str, permission: PermissionCreate, user: User = Depends(getCurrentActivateUser)): 
    permission_get = update_permission(id_permission, permission)
    return{
        "permission": permissionSchema(permission_get),
        "mensaje": "Update Permission"
    }
@permission.delete("/{id_permission}/delete-permission")
async def permission_delete(id_permission:str, user: User = Depends(getCurrentActivateUser)):
    permissio_delete_id= delete_permission(id_permission)
    return{
        "Permission delete:": permissionSchema(permissio_delete_id)
    }