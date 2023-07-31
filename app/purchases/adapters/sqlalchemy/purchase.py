import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
  pass

class Purchase(Base):
    __tablename__ = "purchases"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=True, default=uuid.uuid4())
    purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=False,  default=datetime.utcnow)
    amount_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)