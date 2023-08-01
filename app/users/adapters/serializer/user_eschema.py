from app.users.adapters.sqlalchemy.user import User,Role, Permission, PermissionsRoles


def UserScheam(user: User)-> dict:
    return{
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "pasword":user.password,
        "status":user.status,
        "id_role":user.id_role
    }
    

def UsersSchema(users: list[User])->list:
    return[UsersSchema[user] for user in users]



def RoleSchema(role: Role)-> dict:
    return{
        "id":role.id,
        "name":role.name,
        "status":role.status,
        
    }

def RolesSchema(roles: list[Role])->list:
    return[RoleSchema[role] for role in roles]



def PermissionSchema(permission: Permission)-> dict:
    return{
        "id":permission.id,
        "name":permission.name,
   
    }
def PermossionsSchema(permissions: list[Permission])->list:
    return[PermissionSchema[permission] for permission in permissions]




def PermissionsRolesSchema(permisisonsroles: PermissionsRoles)-> dict:
    return{
        "id_role":permisisonsroles.id_role,
        "id_permission":permisisonsroles.id_permission
   
    }

def PermissionsRolesSchema(permissionsroles: list[PermissionsRoles])-> list:
    return[PermissionsRolesSchema[permissionsroles] for permissionsroles in permissionsroles]