import uuid
from sqlalchemy import select, desc
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.users.domain.pydantic.user import UserCreate, UserUpdate
from app.users.adapters.sqlalchemy.user import User
from app.users.adapters.serializer.user_eschema import User, usersSchema
from app.roles.adapters.services.services import get_id_role
from app.users.adapters.exceptions.exceptions import Nouser, RequieredUser,UserExists,UserExistsEmail
from app.auth.adapters.services.hashed import get_password_hash
session = SessionLocal()


# ----------------------------------USERS SERVICES-----------------------------------------------
    
    
    

def get_users(limit:int, offset:int, status:bool=True):
    # users = session.scalars(select(User).order_by(desc(User.name))).all()
    users = session.scalars(select(User).where(User.status == status).offset(offset).limit(limit).order_by(desc(User.name))).all()
    print(users)
    if not users:
        []
    return users




def post_user(user : UserCreate):
    if not user:
        Nouser()
    if  user.name == "" or user.email == ""  or user.password == "" or user.id_role=="":
        RequieredUser()
        
    usersExis= session.scalars(select(User.document)).all()
    usersExiseamil= session.scalars(select(User.email)).all()
    
    if user.document in usersExis:
        UserExists()
    if user.email in usersExiseamil:
        UserExistsEmail()
        
    role_id_get_role= get_id_role(user.id_role)
    
    password_hashed = get_password_hash(user.password)
    
    new_user = User(name=user.name, document_type=user.document_type, document=user.document, phone=user.phone, email=user.email, password=password_hashed , id_role =role_id_get_role.id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


            

def get_user_id(id_user:str):
    user_id= session.scalars(select(User).filter(User.id == uuid.UUID(id_user))).one()
    if not user_id:
        Nouser()
    return user_id
    
    
def user_update(id_user:str , user: UserUpdate):
    
    
    usersExis= session.scalars(select(User.name).where(User.id != id_user)).all()
    usersExiseamil= session.scalars(select(User.email).where(User.id != id_user)).all()
    if user.document in usersExis:
        UserExists()
    if user.email in usersExiseamil:
        UserExistsEmail()
        
    if not user:
        RequieredUser()
    user_id_update= get_user_id(id_user)   
    user_id_update.name =user.name
    user_id_update.document_type =user.document_type
    user_id_update.document =user.document
    user_id_update.email= user.email
    user_id_update.id_role= user.id_role
    session.commit()
    session.refresh(user_id_update)
    return user_id_update


def delete_user(id_user:str):
    user_detelete_id = get_user_id(id_user)
    session.delete(user_detelete_id)
    session.commit()
    return user_detelete_id

def updateStatusUser(id_user:str):
    user= get_user_id(id_user)
    user.status = not user.status
    session.add(user)
    session.commit()
    return user
    
    