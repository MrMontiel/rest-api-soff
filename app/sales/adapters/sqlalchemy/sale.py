import uuid
from enum import Enum as PyEnum 
from typing import List
from datetime import datetime
from sqlalchemy import Boolean, Enum, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
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
  
  sale_id:Mapped[str] = mapped_column(ForeignKey("sales.id"), primary_key=True)
  product_id:Mapped[str] = mapped_column(ForeignKey("products.id"), primary_key=True)
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