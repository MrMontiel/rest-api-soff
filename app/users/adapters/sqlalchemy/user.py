import  uuid
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app.infrastructure.database import Base
from app.roles.adapters.sqlalchemy.role import Role
from app.auth.adapters.sqlalchemy.models import RecoverPassword


class User(Base):
  __tablename__= "users"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  document_type:Mapped[str]= mapped_column(String(60), nullable=False)
  document:Mapped[str]= mapped_column(String(30), nullable=False, unique=True)
  phone:Mapped[str]= mapped_column(String(15), nullable=False)
  email : Mapped[str]= mapped_column(String, nullable=True, unique=True)
  password : Mapped[str] = mapped_column(String, nullable= True )
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)
  id_role: Mapped[str] = mapped_column(ForeignKey("roles.id"))
  role : Mapped["Role"] = relationship()
  recoveries: Mapped["RecoverPassword"] = relationship()