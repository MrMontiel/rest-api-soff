import uuid
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.supplies.adapters.sqlalchemy.supply import Supplie

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    price: Mapped[float] = mapped_column(float, nullable=False)
    sale_price: Mapped[float] = mapped_column(float, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

class Association(Base):
    __tablename__ = "recipe_detail"

    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), primary_key=True)
    supply_id: Mapped[str] = mapped_column(ForeignKey("supplies.id"), primary_key=True)
    supply: Mapped["Supplie"] = relationship()
    amount_supply: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_measure: Mapped[str] = mapped_column(String(10), nullable=False)



