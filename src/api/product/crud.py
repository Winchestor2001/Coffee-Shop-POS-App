from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import InventoryItem
from src.db.models import Product, ProductIngredient


async def add_product_obj(session: AsyncSession, product_data: dict) -> Product:
    product_obj = Product(**product_data)
    session.add(product_obj)
    await session.commit()
    return product_obj


async def add_product_ingredient_obj(session: AsyncSession, ingredients: list, product_id: str) -> None:
    for item in ingredients:
        item['product_id'] = product_id
        product_ingredient_obj = ProductIngredient(**item)
        session.add(product_ingredient_obj)
        await session.commit()


async def get_product_obj(session: AsyncSession, product_id: str) -> Product:
    stmt = select(Product).filter(
        Product.obj_state == 1, Product.id == product_id
    ).options(
        selectinload(Product.ingredients).selectinload(ProductIngredient.inventory)
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_products_obj(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product).filter(
        Product.obj_state == 1
    ).options(
        selectinload(Product.ingredients).selectinload(ProductIngredient.inventory)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_product_obj(session: AsyncSession, product_id: str, product_data: dict) -> None:
    stmt = update(Product).where(Product.id == product_id, Product.obj_state == 1).values(**product_data)
    await session.execute(stmt)
    await session.commit()


async def remove_product_obj(session: AsyncSession, product_id: str):
    stmt = delete(Product).where(Product.id == product_id, Product.obj_state == 1)
    await session.execute(stmt)
    await session.commit()