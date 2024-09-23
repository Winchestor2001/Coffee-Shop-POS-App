from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.base import Base, BaseMixin


# class LoyaltyProgram(Base, BaseMixin):
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#     points: Mapped[int] = mapped_column(Integer, default=0)
#
#     user: Mapped["User"] = relationship("User", back_populates="loyalty_program")
