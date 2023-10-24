import uuid
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.infrastructure.database import Base

class Provider(Base):
  __tablename__ = "providers"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nit: Mapped[str] = mapped_column(String, nullable=False) 
  name: Mapped[str] = mapped_column(String, nullable=False)
  company: Mapped[str] = mapped_column(String, nullable=False)
  address: Mapped[str] = mapped_column(String, nullable=False)
  date_registration: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow) 
  # email: Mapped[str] = mapped_column(String, nullable=False)
  phone: Mapped[str] = mapped_column(String)
  city: Mapped[str] = mapped_column(String, nullable=False)
  status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)