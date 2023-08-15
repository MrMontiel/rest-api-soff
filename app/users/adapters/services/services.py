import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import ConectDatabase
from app.users.domain.pydantic.user import UserCreate, RoleCreate, PermissionCreate
from app.users.adapters.sqlalchemy.user import User, Role
from app.users.adapters.serializer.user_eschema import User, usersSchema

session = ConectDatabase.getInstance()



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
    roles = session.scalars(select(Role).where(Role.id==id_role)).one()
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
    if user.email == ""  or user.name == "" or user.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the fields name, email and password ")
    
    
    get_id_role(user.id_role)
    new_user = User(name=user.name,  email=user.email, password= user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
            

