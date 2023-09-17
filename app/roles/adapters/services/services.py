import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.roles.domain.pydantic.role import RoleCreate, PermissionsRolesCreate
from app.roles.adapters.sqlalchemy.role import Role, PermissionsRoles
from app.users.adapters.sqlalchemy.user import User


session = SessionLocal()


# ----------------------------------ROLE SERVICES-----------------------------------------------
def get_roles(limit:int = 10):
    roles = session.scalars(select(Role)).all()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return roles


def create_rol(role: RoleCreate):
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role is required")
    if role.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name is required ")
    new_role = Role(name= role.name)
    
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role



def get_id_role(id_role:str):
    roles = session.scalars(select(Role).where(Role.id== id_role)).one()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return roles



def update_role(role: RoleCreate, id_role:str):
    
    role_update = session.query(Role).filter(Role.id == uuid.UUID(id_role)).first()
    if not role_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    role_update.name = role.name
    session.commit()
    session.refresh(role_update)
    return role_update
    
# --------------------------------------ROLE REPLACE------------------------------------------------
def replace_role_base(id_role:str):
    permissionroles = session.scalars(select(PermissionsRoles).filter(PermissionsRoles.id_role == uuid.UUID(id_role))).all()
    for permissions in permissionroles:
        session.delete(permissions)
        session.commit
        
    user_replce= session.scalars(select(User).filter(User.id_role== uuid.UUID(id_role))).all()
    role_replce_new= session.scalars(select(Role).filter(Role.name== "Base")).one()
    for user in user_replce:
        user.id_role=role_replce_new.id
        session.add(user)
        session.commit()
    
# --------------------------------------ROLE------------------------------------------------

def delete_role_service(id_role:str):
    article_query =  session.query(Role).filter(Role.id == uuid.UUID(id_role)).first()
    if not article_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    replace_role_base(id_role)
    
    session.delete(article_query)
    session.commit()
    return article_query

# ----------------------------------ROLEPERMISSION SERVICES-----------------------------------------------



def permissionroles_get(id_permissionrole:str):
    if not id_permissionrole:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission Role is required")
    permissionrole_get =session.scalars(select(PermissionsRoles).filter(PermissionsRoles.id_role == id_permissionrole)).all()
    if not permissionrole_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission Role not found")
    return(permissionrole_get)

def permissionsrole_create(permissionsrole: PermissionsRolesCreate):
    if not permissionsrole:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is required")
    if permissionsrole.id_permission == ""  or permissionsrole.id_role == "" :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the id Permission and id rol is required")
        
    new_permissionsrole= PermissionsRoles(id_permission = permissionsrole.id_permission, id_role = permissionsrole.id_role)
    session.add(new_permissionsrole)
    session.commit()
    session.refresh(new_permissionsrole)
    return new_permissionsrole