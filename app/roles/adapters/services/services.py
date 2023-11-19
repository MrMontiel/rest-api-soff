import uuid
from sqlalchemy import select, desc,delete
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.roles.domain.pydantic.role import RoleCreate, PermissionsRolesCreate
from app.roles.adapters.sqlalchemy.role import Role, PermissionsRoles
from app.users.adapters.sqlalchemy.user import User
from app.roles.adapters.exceptions.exections import NoUpdateStatusRole,Norole, Requieredrol, roleExists,noDeleteRole
from app.roles.adapters.serializer.roles_schema import permissionsRolesSchema
from sqlalchemy.exc import PendingRollbackError

session = SessionLocal()


# ----------------------------------ROLE SERVICES-----------------------------------------------
def get_roles(limit:int, offset:int, status:bool=True):
    try:
        roles = session.scalars(select(Role).where(Role.status == status).offset(offset).order_by(desc(Role.name))).all()
        if not roles:
            []
        return roles
    except PendingRollbackError as e:
        session.rollback()


def create_rol(role: RoleCreate):
    if not role:
        Requieredrol()
    if role.name == "":
        Requieredrol()
    try:
        new_role = Role(name= role.name)
        
        session.add(new_role)
        session.commit()
        session.refresh(new_role)
        return new_role
    except PendingRollbackError as e:
        session.rollback()


def get_id_role(id_role:str):
    try:
        roles = session.scalars(select(Role).where(Role.id== uuid.UUID(id_role))).one()
        if not roles:
            Norole()
        return roles
    except PendingRollbackError as e:
        session.rollback()
        


def update_role(name:str, id_role:str):
    
    try:
        roleExi= session.scalars(select(Role.name).where(Role.id != id_role)).all()
        if name in roleExi:
            roleExists()
        role_update = session.query(Role).filter(Role.id == uuid.UUID(id_role)).first()
        if not role_update:
            Norole()    
        role_update.name = name
        session.commit()
        session.refresh(role_update)
        return role_update
    except PendingRollbackError as e:
        session.rollback()
# --------------------------------------ROLE REPLACE------------------------------------------------
def replace_role_base(id_role:str):
    try:
        permissionroles = session.scalars(select(PermissionsRoles).filter(PermissionsRoles.id_role == uuid.UUID(id_role))).all()
        for permissions in permissionroles:
            session.delete(permissions)
            session.commit()
            
        user_replce= session.scalars(select(User).filter(User.id_role== uuid.UUID(id_role))).all()
        role_replce_new= session.scalars(select(Role).filter(Role.name== "Base")).one()
        for user in user_replce:
            user.id_role=role_replce_new.id
            session.add(user)
            session.commit()
    except PendingRollbackError as e:
        session.rollback()        
# --------------------------------------ROLE------------------------------------------------

def delete_role_service(id_role:str):
    try:
        article_query =  session.query(Role).filter(Role.id == uuid.UUID(id_role)).first()
        
        if article_query.name == "Administrador" or article_query.name == "Base":
            noDeleteRole()
        if not article_query:
            Norole()
        replace_role_base(id_role)
        
        session.delete(article_query)
        session.commit()
        return article_query
    except PendingRollbackError as e:
        session.rollback()
# ----------------------------------ROLEPERMISSION SERVICES-----------------------------------------------



def permissionroles_get(id_permissionrole:str):
    try:
        if not id_permissionrole:
            Requieredrol()
        permissionrole_get =session.scalars(select(PermissionsRoles).filter(PermissionsRoles.id_role == id_permissionrole)).all()
        if not permissionrole_get:
            []
        return permissionrole_get
    except PendingRollbackError as e:
        session.rollback()
        
        
def permissionsrole_create(permissionsrole: PermissionsRolesCreate):
    try:
        
        if not permissionsrole:
            Requieredrol()
        if permissionsrole.id_permission == ""  or permissionsrole.id_role == "" :
            Requieredrol()        
        new_permissionsrole= PermissionsRoles(id_permission = permissionsrole.id_permission, id_role = permissionsrole.id_role)
        session.add(new_permissionsrole)
        session.commit()
        session.refresh(new_permissionsrole)
        return new_permissionsrole
    except PendingRollbackError as e:
        session.rollback()
        
        
def Permission_role_create(nombre_role:str, permissions):
    try:
        roleExi=session.scalars(select(Role.name)).all()
        if nombre_role in roleExi:
            roleExists()


        new_role = Role(name=nombre_role)
        session.add(new_role)
        session.commit()
        session.refresh(new_role)
        if not new_role:
            Norole()
        for permission in permissions:
            permission_database = PermissionsRoles(id_role=new_role.id, id_permission=permission.id_permission)
            session.add(permission_database)
            session.commit()
    except PendingRollbackError as e:
        session.rollback()
        
        
def updateStatusRole(id_role:str):
    try:
        role = session.get(Role, uuid.UUID( id_role))
        if not role:
            Norole()
        
        if role.name == "Administrador" or role.name== "Base":
            NoUpdateStatusRole()
            
        role.status= not role.status
        session.add(role)
        session.commit()
        return role
    except PendingRollbackError as e:
        session.rollback()   

# -----------------------UPDATEROLESPERMISSIONS---------------------------
def updateRolesPermissions(id_rol:str,permissions):
    try:
        if permissions:
            permiisions_query =  session.query(PermissionsRoles).all()
            delete_stmt = delete(PermissionsRoles).where(PermissionsRoles.id_role == id_rol)
            session.execute(delete_stmt)
            session.commit()
            for permission in permissions:
                permission_database = PermissionsRoles(id_role=id_rol, id_permission=permission.id_permission)
                session.add(permission_database)
                session.commit()
        else:
            Norole()
    except PendingRollbackError as e:
        session.rollback()