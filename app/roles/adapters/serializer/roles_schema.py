from app.roles.adapters.sqlalchemy.role import Role, PermissionsRoles

def roleSchema(role: Role)-> dict:
    return{
        "id":role.id,
        "name":role.name,
        "status":role.status,
    }

def rolesSchema(roles: list[Role])->list:
    return[roleSchema(role) for role in roles]


def permissionRolesSchema(permisisonsroles: PermissionsRoles)-> dict:
    return{
        "id_role":permisisonsroles.id_role,
        "id_permission":permisisonsroles.id_permission
    }

def permissionsRolesSchema(permissionsroles: list[PermissionsRoles])-> list:
    return[permissionRolesSchema(permissionsroles) for permissionsroles in permissionsroles]
