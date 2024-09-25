import logging
from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.product import schemas, crud
from src.api.user.utils import JwtBearer, role_check
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/category/add", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
             response_model=schemas.AddProductCategory)
async def add_product(
        category_data: schemas.AddProductCategory,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        token: str = Depends(JwtBearer())):
    category_obj = await crud.add_category_obj(session, category_data.name)
    return category_obj


@router.post("/add", dependencies=[Depends(JwtBearer()), Depends(role_check(["barman", "admin"]))],
             response_model=schemas.ProductInfo)
async def add_product(
        product_data: schemas.AddProduct,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        token: str = Depends(JwtBearer())):
    ingredients = [item.model_dump() for item in product_data.ingredients]
    product_data_dict = product_data.model_dump()

    product_data_dict.pop("ingredients")

    product_obj = await crud.add_product_obj(session, product_data_dict)
    await crud.add_product_ingredient_obj(session, ingredients, product_obj.id)
    product = await crud.get_product_obj(session, product_obj.id)
    return product


@router.get("/category/list", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=List[schemas.ProductCategoryInfo])
async def products_list(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    categories = await crud.get_categories_obj(session)
    return categories


@router.get("/list", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=List[schemas.ProductInfo])
async def products_list(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    products = await crud.get_products_obj(session)
    return products


@router.put("/update/{product_id}", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=schemas.ProductUpdate)
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


@router.delete("/remove/{product_id}", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
               response_model=Dict[str, str])
async def remove_product(
        product_id: str,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    await crud.remove_product_obj(session, product_id)
    return {"detail": f"Product: {product_id} removed successfully"}
