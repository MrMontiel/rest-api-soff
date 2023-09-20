import  uuid
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app.permissions.adapters.slqalchemy.permission import Permission
from app.infrastructure.database import Base

class Role(Base):
  __tablename__= "roles"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  Permissions: Mapped[List["PermissionsRoles"]]= relationship()
  
  
class PermissionsRoles(Base):
  __tablename__ ="permission_role"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  id_role : Mapped[str] = mapped_column(ForeignKey("roles.id"), primary_key=True)
  id_permission: Mapped[str] = mapped_column(ForeignKey("permissions.id"), primary_key=True)
  Permission: Mapped["Permission"] = relationship()