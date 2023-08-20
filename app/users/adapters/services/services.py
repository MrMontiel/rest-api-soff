import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.users.domain.pydantic.user import UserCreate, RoleCreate, PermissionCreate, PermissionsRolesCreate
from app.users.adapters.sqlalchemy.user import User, Role, Permission, PermissionsRoles
from app.users.adapters.serializer.user_eschema import User, usersSchema, permissionsRolesSchema

session = SessionLocal()

# ----------------------------------PERMISSION SERVICES-----------------------------------------------

def get_permission(limit:int = 10):
    get_permissions = session.scalars(select(Permission)).all()
    if not get_permissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return get_permissions



def create_permission(permission: PermissionCreate):
    if not permission:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is required")
    if permission.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is required")
    new_permission = Permission(name=permission.name)
    session.add(new_permission)
    session.commit()
    session.refresh(new_permission)
    return new_permission

def get_id_permission(id_permission: str):
    permission_id= session.scalars(select(Permission).where(Permission.id == id_permission)).one()
    if not permission_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return permission_id   
    
def update_permission(id_permission:str, permission: PermissionCreate):
    permission_update = session.query(Permission).filter(Permission.id == uuid.UUID(id_permission)).first()
    if not permission_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    permission_update.name = permission.name
    session.commit()
    session.refresh(permission_update)
    return permission_update

def delete_permission(id_permission: str):
    permission_delete= session.scalars(select(Permission).where(Permission.id == uuid.UUID(id_permission))).one()
    if not permission_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permision not found")
    session.delete(permission_delete)
    session.commit()
    return permission_delete
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
    

def delete_role_service(id_role:str):
    article_query =  session.query(Role).filter(Role.id == id_role).first()
    if not article_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
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

# ----------------------------------USERS SERVICES-----------------------------------------------
    
    
    

def get_users(limit:int = 100):
    users = session.scalars(select(User)).all()
    print(users)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="users not found")
    return users




def post_user(user : UserCreate):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is required")
    if  user.name == "" or user.email == ""  or user.password == "" or user.id_role=="":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the fields name, email and password ")
    role_id_get_role= get_id_role(user.id_role)
    new_user = User(name=user.name,  email=user.email, password= user.password , id_role = role_id_get_role.id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


            

def get_user_id(id_user:str):
    user_id= session.scalars(select(User).filter(User.id == id_user)).one()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="users not found")
    return user_id
    
    
def user_update(id_user:str , user: UserCreate):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is required")
    user_id_update= get_user_id(id_user)
    user_id_update.name =user.name
    user_id_update.email= user.email
    user_id_update.password= user.password
    user_id_update.id_role= user.id_role
    session.commit()
    session.refresh(user_id_update)
    return user_id_update


def delete_user(id_user:str):
    user_detelete_id = get_user_id(id_user)
    session.delete(user_detelete_id)
    session.commit()
    return user_detelete_id

# --------------------------------------------------------------------------------------
def replace_role_base(id_role):
    user_replce= session.scalars(select(User).filter(User.id_role== id_role)).all()
    role_replce= session.scalars(select(Role).filter(Role.id== id_role)).one()
    role_replce_new= session.scalars(select(Role).filter(Role.name== "Base")).one()
    for ban in user_replce:
        ban.id_role=role_replce_new.id
        session.add(user_replce)
        session.commit()
    return user_replce 