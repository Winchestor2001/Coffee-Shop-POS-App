from typing import List

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.api.inventory.schemas import InventoryInfo
from src.db.utils import SizeEnum, ColorEnum, IngredientUnitEnum


class ProductIngredientSchema(BaseModel):
    inventory_id: str
    quantity: float
    unit: IngredientUnitEnum


class ProductIngredientInfo(BaseModel):
    id: str
    quantity: float
    extra_item: bool
    unit: IngredientUnitEnum
    inventory: InventoryInfo


class AddProductCategory(BaseModel):
    name: str


class AddProduct(BaseModel):
    name: str
    description: str | None = None
    price: float
    category_id: str
    color: ColorEnum
    size: SizeEnum
    ingredients: List[ProductIngredientSchema]


class ProductInfo(AddProduct):
    id: str
    ingredients: List[ProductIngredientInfo]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductCategoryInfo(AddProductCategory):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(AddProduct):
    pass