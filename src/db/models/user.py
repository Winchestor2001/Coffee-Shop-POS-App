from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    loyalty_program: Mapped["LoyaltyProgram"] = relationship("LoyaltyProgram", back_populates="user")
