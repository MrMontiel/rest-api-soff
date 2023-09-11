import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.users.domain.pydantic.user import UserCreate
from app.users.adapters.sqlalchemy.user import User
from app.users.adapters.serializer.user_eschema import User, usersSchema
from app.roles.adapters.services.services import get_id_role

session = SessionLocal()


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

