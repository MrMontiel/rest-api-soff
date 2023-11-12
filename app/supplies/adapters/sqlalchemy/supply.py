import uuid

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.infrastructure.database import Base


class Supply(Base):
  __tablename__ = "supplies"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String, nullable=False, unique=True) 
  price: Mapped[float] = mapped_column(Float, nullable=False)
  quantity_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  unit_measure: Mapped[str] = mapped_column(String, nullable=False)
  total: Mapped[str] = mapped_column(Float, nullable=False)
  status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)