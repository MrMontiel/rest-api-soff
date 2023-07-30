import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    price: Mapped[float] = mapped_column(float, nullable=False)
    sale_price: Mapped[float] = mapped_column(float, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)