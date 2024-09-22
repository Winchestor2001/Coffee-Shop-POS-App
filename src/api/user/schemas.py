import re
import datetime

from pydantic import BaseModel, field_validator, ConfigDict

from src.settings import settings


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
    phone_number: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


