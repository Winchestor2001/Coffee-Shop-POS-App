from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base, BaseMixin
from src.db.utils import ItemEnum


class InventoryItem(Base, BaseMixin):
    product_name: Mapped[str]
    quantity: Mapped[int]
    unit: Mapped[ItemEnum] = mapped_column(nullable=False)
