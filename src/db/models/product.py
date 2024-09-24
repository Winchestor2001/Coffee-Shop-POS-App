from typing import TYPE_CHECKING, List
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, BaseMixin
from src.db.utils import SizeEnum, ColorEnum

if TYPE_CHECKING:
    from src.db.models import InventoryItem


class Product(Base, BaseMixin):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    color: Mapped[ColorEnum] = mapped_column(nullable=False)

    ingredients: Mapped[List["ProductIngredient"]] = relationship(back_populates="product")


class ProductIngredient(Base, BaseMixin):
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    inventory_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"), nullable=False)
    quantity: Mapped[float]
    size: Mapped[SizeEnum] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="ingredients")
    inventory: Mapped["InventoryItem"] = relationship(back_populates="product_ingredient")
