import logging
from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.inventory import schemas, crud
from src.api.user.utils import JwtBearer, role_check
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/add", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
             response_model=schemas.InventoryInfo)
async def add_inventory(
        product_data: schemas.AddInventory,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]):
    inventory_obj = await crud.add_product_to_inventory_obj(session, product_data.model_dump())
    return inventory_obj


@router.get("/list", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=List[schemas.InventoryInfo])
async def inventory_list(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]):
    inventory_objs = await crud.get_inventory_list_obj(session)
    return inventory_objs


@router.put("/update", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=schemas.UpdateInventory)
async def inventory_update(
        inventor_id: str,
        inventor_data: schemas.UpdateInventory,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]):
    await crud.update_inventory_obj(session, inventor_id, inventor_data.model_dump())
    return inventor_data


@router.delete("/remove/{inventory_id}", dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
               response_model=Dict[str, str])
async def remove_inventory(
        inventory_id: str,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    await crud.remove_inventory_obj(session, inventory_id)
    return {"detail": f"Inventory: {inventory_id} removed successfully"}
