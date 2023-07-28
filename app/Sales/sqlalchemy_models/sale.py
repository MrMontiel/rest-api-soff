from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


from app.config.database import Base

class Sale(Base):
  __tablename__ = 'sales'
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_date = Column(DateTime, default=datetime.utcnow)
  amount_order = Column(Integer, nullable=False, default=0)
  pyment_method = Column(String, nullable=False)
  type_sale = Column(String, nullable=False)
  total = Column(Float, nullable=False, default=0.0) 
  status = Column(Boolean, nullable=False, default=True)
  
  orders = relationship("SalesOrders", back_populates="sale")

class ProductFail(Base):
  __tablename__ = 'products'
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  
  orders = relationship("SalesOrders", back_populates="product")

class SalesOrders(Base):
  __tablename__ = 'sales_orders'
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
  product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
  amount_product = Column(Integer, nullable=False)
  total = Column(Float, nullable=False, default=0.0) 
  
  sale = relationship("Sale", back_populates="orders")
  product = relationship("ProductFail", back_populates="orders")