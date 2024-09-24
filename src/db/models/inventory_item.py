from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base, BaseMixin
from src.db.utils import ItemEnum

if TYPE_CHECKING:
    from src.db.models import ProductIngredient


class InventoryItem(Base, BaseMixin):
    product_name: Mapped[str]
    quantity: Mapped[int]
    unit: Mapped[ItemEnum] = mapped_column(nullable=False)

    product_ingredient: Mapped["ProductIngredient"] = relationship(back_populates="inventory")
