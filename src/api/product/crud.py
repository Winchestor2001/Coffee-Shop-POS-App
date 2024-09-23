from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Product


async def add_product_obj(session: AsyncSession, product_data: dict) -> Product:
    product_obj = Product(**product_data)
    session.add(product_obj)
    await session.commit()
    return product_obj


async def get_products_obj(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_product_obj(session: AsyncSession, product_id: str, product_data: dict) -> None:
    stmt = update(Product).where(Product.id == product_id).values(**product_data)
    await session.execute(stmt)
    await session.commit()


async def remove_product_obj(session: AsyncSession, product_id: str):
    stmt = delete(Product).where(Product.id == product_id)
    await session.execute(stmt)
    await session.commit()