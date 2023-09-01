from app.users.adapters.sqlalchemy.user import User,Role, Permission, PermissionsRoles

def userSchema(user: User)-> dict:
    return{
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "pasword":user.password,
        "status":user.status,
        "id_role":user.id_role
    }
    
def usersSchema(users: list[User])->list:
    return[userSchema(user) for user in users]



def roleSchema(role: Role)-> dict:
    return{
        "id":role.id,
        "name":role.name,
        "status":role.status,
    }

def rolesSchema(roles: list[Role])->list:
    return[roleSchema(role) for role in roles]

def permissionSchema(permission: Permission)-> dict:
    return{
        "id":permission.id,
        "name":permission.name,
    }
    
def PermissionsSchema(permissions: list[Permission])->list:
    return[permissionSchema(permission) for permission in permissions]




def permissionRolesSchema(permisisonsroles: PermissionsRoles)-> dict:
    return{
        "id_role":permisisonsroles.id_role,
        "id_permission":permisisonsroles.id_permission
   
    }

def permissionsRolesSchema(permissionsroles: list[PermissionsRoles])-> list:
    return[permissionRolesSchema(permissionsroles) for permissionsroles in permissionsroles]
