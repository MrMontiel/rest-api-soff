import uuid
from typing import List
from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

uuidType = uuid.UUID

class Base(DeclarativeBase):
  pass

class Sale(Base):
  __tablename__ = 'sales'
  
  id: Mapped[uuidType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
  amount_order:Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  pyment_method:Mapped[str] = mapped_column(String, nullable=False)
  type_sale:Mapped[str] = mapped_column(String, nullable=False)
  total:Mapped[float] = mapped_column(Float, nullable=False, default=0.0) 
  status:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
  
  orders:Mapped[List["SalesOrders"]] = relationship()

class SalesOrders(Base):
  __tablename__ = 'sales_orders'
  
  id: Mapped[uuidType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_id:Mapped[uuidType] = mapped_column(ForeignKey("sales.id"))
  amount_product:Mapped[int] = Column(Integer, nullable=False)
  total:Mapped[float] = Column(Float, nullable=False, default=0.0) 