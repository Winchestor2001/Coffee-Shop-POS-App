from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.db.utils import ItemEnum


class AddInventory(BaseModel):
    product_name: str
    quantity: int
    unit: ItemEnum


class UpdateInventory(AddInventory):
    pass


class InventoryInfo(BaseModel):
    product_name: str
    quantity: int
    unit: ItemEnum
