from sqlalchemy import DateTime, Text, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.db.base import Base


class Report(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)
