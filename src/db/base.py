from datetime import datetime

import pytz
from sqlalchemy import String, Column, TIMESTAMP, MetaData, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.db.utils import camel_case_to_snake_case, generate_uuid
from src.settings import settings


class BaseMixin:
    uuid = Column(String(36), nullable=False, default=generate_uuid, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(pytz.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(pytz.utc)
    )
    obj_state = Column(Integer(), default=1)


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
