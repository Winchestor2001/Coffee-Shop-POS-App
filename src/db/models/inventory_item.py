from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base, BaseMixin


class InventoryItem(Base, BaseMixin):
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="inventory")
