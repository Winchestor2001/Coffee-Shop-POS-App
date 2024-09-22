import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user import schemas, utils, crud
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/regtest")
async def authenticate_user(
        auth_data: schemas.AuthUser,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]):
    user_obj = await crud.create_user_obj(session, auth_data.model_dump())
    return user_obj


@router.post("/auth")
async def authenticate_user(
        auth_data: schemas.AuthUser,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    user_obj = await crud.get_user_info_obj(session, auth_data.phone_number)
    if await utils.verify_password(auth_data.password, user_obj.password):
        token_data = {"id": user_obj.id}
        access_token = utils.JwtBearer.create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")


@router.get("/info", dependencies=[Depends(utils.JwtBearer())], response_model=schemas.UserInfo)
async def user_info(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        token: str = Depends(utils.JwtBearer()),

):
    user_id = utils.JwtBearer.verify_access_token(token)["id"]
    user_obj = await crud.get_user_info_obj(session, user_id=user_id)
    return user_obj
