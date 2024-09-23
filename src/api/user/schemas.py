import re
import datetime

from pydantic import BaseModel, field_validator, ConfigDict

from src.db.utils import UserRoleEnum
from src.settings import settings


class RegTest(BaseModel):
    full_name: str
    phone_number: str
    password: str

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(settings.pattern, value):
            raise ValueError("Invalid phone number format")
        return value


class AuthUser(BaseModel):
    phone_number: str
    password: str

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(settings.pattern, value):
            raise ValueError("Invalid phone number format")
        return value


class UserInfo(BaseModel):
    id: str
    full_name: str
    phone_number: str
    user_role: UserRoleEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
