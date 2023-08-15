import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List

from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.infrastructure.database import Base
from app.products.adapters.sqlalchemy.product import Product


class StatusSale(PyEnum):
  OPEN = "open"
  PAID = "paid"
  CANCEL = "cancel"
  PENDING = "pending"


class Sale(Base):
  __tablename__ = 'sales'
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
  amount_order:Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  pyment_method:Mapped[str] = mapped_column(String, nullable=False)
  id_client: Mapped[str] = mapped_column(ForeignKey("clients.id"))
  client: Mapped["Client"] = relationship()
  type_sale:Mapped[str] = mapped_column(String, nullable=False)
  total:Mapped[float] = mapped_column(Float, nullable=False, default=0.0) 
  status:Mapped[str] = mapped_column(Enum(StatusSale), nullable=False, default=StatusSale.OPEN)
  
  products: Mapped[List["SalesOrders"]] =  relationship()


class SalesOrders(Base):
  __tablename__ = 'sales_orders'
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_id:Mapped[str] = mapped_column(ForeignKey("sales.id"))
  product_id:Mapped[str] = mapped_column(ForeignKey("products.id"))
  product: Mapped["Product"] = relationship()
  amount_product:Mapped[int] = Column(Integer, nullable=False)
  total:Mapped[float] = Column(Float, nullable=False, default=0.0)
  
class Client(Base):
  __tablename__ = 'clients'
  
  id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String(60), nullable=False)
  direction: Mapped[str] = mapped_column(String(60), nullable=False)
  phone: Mapped[str] = mapped_column(String(60), nullable=False)
  email: Mapped[str] = mapped_column(String(60), nullable=False)