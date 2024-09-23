from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import InventoryItem


async def add_product_to_inventory_obj(session: AsyncSession, product_data: dict) -> InventoryItem:
    inventory_obj = InventoryItem(**product_data)
    session.add(inventory_obj)
    await session.commit()
    return inventory_obj


async def get_inventory_list_obj(session: AsyncSession) -> Sequence[InventoryItem]:
    stmt = select(InventoryItem).filter(InventoryItem.obj_state == 1)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_inventory_obj(session: AsyncSession, inventor_id: str, inventor_data: dict):
    stmt = update(InventoryItem).where(InventoryItem.id == inventor_id, InventoryItem.obj_state == 1).values(
        **inventor_data)
    await session.execute(stmt)
    await session.commit()


async def remove_inventory_obj(session: AsyncSession, inventor_id: str):
    stmt = delete(InventoryItem).where(InventoryItem.id == inventor_id)
    await session.execute(stmt)
    await session.commit()
