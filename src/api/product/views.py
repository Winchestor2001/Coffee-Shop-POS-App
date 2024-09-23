import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.product import schemas, crud
from src.api.user.utils import JwtBearer, role_check
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/add", dependencies=[Depends(JwtBearer()), Depends(role_check(["barman", "admin"]))])
async def add_product(
        product_data: schemas.AddProduct,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        token: str = Depends(JwtBearer())):
    product_obj = await crud.add_product_obj(session, product_data.model_dump())
    return product_obj


@router.get("/list", response_model=List[schemas.ProductInfo])
async def products_list(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    products = await crud.get_products_obj(session)
    return products


@router.put("/update/{product_id}", dependencies=[Depends(JwtBearer()), Depends(role_check(["barman", "admin"]))])
async def update_product(
        product_id: str,
        product_data: schemas.ProductUpdate,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    await crud.update_product_obj(session, product_id, product_data.model_dump())
    return product_data


@router.delete("/remove/{product_id}", dependencies=[Depends(JwtBearer()), Depends(role_check(["barman", "admin"]))])
async def remove_product(
        product_id: str,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    await crud.remove_product_obj(session, product_id)
    return {"detail": f"Product: {product_id} removed successfully"}
