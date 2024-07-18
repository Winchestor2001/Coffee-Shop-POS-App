from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
    inventory: Mapped[list["InventoryItem"]] = relationship("InventoryItem", back_populates="product")
