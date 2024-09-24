from typing import List

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.api.inventory.schemas import InventoryInfo
from src.db.utils import SizeEnum, ColorEnum


class ProductIngredientSchema(BaseModel):
    inventory_id: str
    quantity: float
    size: SizeEnum


class ProductIngredientInfo(BaseModel):
    id: str
    quantity: float
    size: SizeEnum
    inventory: InventoryInfo


class AddProduct(BaseModel):
    name: str
    description: str | None = None
    price: float
    color: ColorEnum
    ingredients: List[ProductIngredientSchema]


class ProductInfo(AddProduct):
    id: str
    ingredients: List[ProductIngredientInfo]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(AddProduct):
    pass