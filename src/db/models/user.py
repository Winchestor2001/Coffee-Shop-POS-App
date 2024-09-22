from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base, BaseMixin


class User(Base, BaseMixin):
    phone_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    loyalty_program: Mapped["LoyaltyProgram"] = relationship("LoyaltyProgram", back_populates="user")
