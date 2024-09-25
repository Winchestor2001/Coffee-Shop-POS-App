from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.db.utils import ItemEnum


class AddInventory(BaseModel):
    product_name: str
    quantity: int
    price: float
    unit: ItemEnum


class UpdateInventory(AddInventory):
    pass


class InventoryInfo(AddInventory):
    id: str
    created_at: datetime
    updated_at: datetime
