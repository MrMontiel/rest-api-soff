import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.providers.adapters.sqlachemy.provider import Provider
from app.infrastructure.database import Base

class Purchase(Base):
  __tablename__ = "purchases"
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=True, default=uuid.uuid4())
  purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=False,  default=datetime.utcnow)
  amount_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  provider_id:Mapped[str] = mapped_column(ForeignKey("providers.id"))
  provider:Mapped["Provider"] = relationship() 
  total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
  status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
class PurchasesOrders(Base):
  __tablename__ = "purchases_orders"
  
  purchase_id: Mapped[str] = mapped_column(ForeignKey("purchases.id"), primary_key=True)
  supply_id: Mapped[str] = mapped_column(ForeignKey("supplies.id"), primary_key=True)
  supply: Mapped["Supply"] = relationship()
  amount_supplies: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  price_supplies: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
  subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
  