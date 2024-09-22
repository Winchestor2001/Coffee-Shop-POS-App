from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.user.utils import hash_password

from src.db.models import User


async def create_user_obj(session: AsyncSession, user_data: dict) -> User:
    user_exists = bool(await get_user_info_obj(session, user_data['phone_number']))
    if user_exists:
        raise ValueError("User with the same phone number already exists")
    user_data['password'] = await hash_password(user_data['password'])
    user_obj = User(**user_data)
    session.add(user_obj)
    await session.commit()
    return user_obj


async def get_user_info_obj(session: AsyncSession, phone_number: str = None, user_id: str = None):
    if user_id:
        stmt = select(User).where(User.id == user_id)
    else:
        stmt = select(User).where(User.phone_number == phone_number)
    result = await session.scalar(stmt)
    return result