from sqlalchemy import String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.base import Base, BaseMixin
from src.db.utils import UserRoleEnum


class User(Base, BaseMixin):
    full_name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    user_role: Mapped[UserRoleEnum] = mapped_column(nullable=False, default=UserRoleEnum.USER)

    # orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    # loyalty_program: Mapped["LoyaltyProgram"] = relationship("LoyaltyProgram", back_populates="user")
