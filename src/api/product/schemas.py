from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AddProduct(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductInfo(AddProduct):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(AddProduct):
    pass