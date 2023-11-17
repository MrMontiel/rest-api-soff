import  uuid
from typing import List
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from app.infrastructure.database import Base


class Permission(Base):
  __tablename__= "permissions"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
  name : Mapped[str]= mapped_column(String(60), nullable=False)
  status : Mapped[bool] = mapped_column(Boolean, nullable=False , default=True)