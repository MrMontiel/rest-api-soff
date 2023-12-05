import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.infrastructure.database import SessionLocal
from app.permissions.domain.pydantic.permission import PermissionCreate
from app.permissions.adapters.slqalchemy.permission import Permission
from app.permissions.adapters.serializer.roles_schema import permissionSchema
from sqlalchemy.exc import PendingRollbackError


session = SessionLocal()

# ----------------------------------PERMISSION SERVICES-----------------------------------------------

def get_permission(limit:int = 10):
    try:
        get_permissions = session.scalars(select(Permission)).all()
        if not get_permissions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return get_permissions
    except PendingRollbackError as e:
        session.rollback()


def create_permission(permission: PermissionCreate):
    try:
        if not permission:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is required")
        if permission.name == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission is required")
        new_permission = Permission(name = permission.name)
        session.add(new_permission)
        session.commit()
        session.refresh(new_permission)
        return new_permission
    except PendingRollbackError as e:
        session.rollback()

def get_id_permission(id_permission: str):
    try:
        permission_id= session.scalars(select(Permission).where(Permission.id == id_permission)).one()
        if not permission_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return permission_id   
    except PendingRollbackError as e:
        session.rollback()
    
def update_permission(id_permission:str, permission: PermissionCreate):
    try:
        
        permission_update = session.query(Permission).filter(Permission.id == uuid.UUID(id_permission)).first()
        if not permission_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        permission_update.name = permission.name
        session.commit()
        session.refresh(permission_update)
        return permission_update
    except PendingRollbackError as e:
        session.rollback()
        
def delete_permission(id_permission: str):
    try:
        permission_delete= session.scalars(select(Permission).where(Permission.id == uuid.UUID(id_permission))).one()
        if not permission_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permision not found")
        session.delete(permission_delete)
        session.commit()
        return permission_delete
    except PendingRollbackError as e:
        session.rollback()
