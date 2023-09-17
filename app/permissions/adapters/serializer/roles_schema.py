from app.permissions.adapters.slqalchemy.permission import Permission

def permissionSchema(permission: Permission)-> dict:
    return{
        "id":permission.id,
        "name":permission.name,
    }
    
def PermissionsSchema(permissions: list[Permission])->list:
    return[permissionSchema(permission) for permission in permissions]


