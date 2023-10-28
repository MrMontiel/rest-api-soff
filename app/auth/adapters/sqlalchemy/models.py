import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base

class RecoverPassword(Base):
  __tablename__ = "recover_password"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id:Mapped[str] = mapped_column(ForeignKey("users.id"))
  code: Mapped[str] = mapped_column(String(6), nullable=False, unique=True)
  apikey: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
  verify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,  default=datetime.utcnow)