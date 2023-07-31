import uuid
from sqlalchemy import String, Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base

class Supply(Base):
  __tablename__ = "supplies"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4())
  name: Mapped[str] = mapped_column(String, nullable=False) 
  price: Mapped[float] = mapped_column(Float, nullable=False)
  quantity_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  unit_measure: Mapped[str] = mapped_column(String, nullable=False)
  status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)