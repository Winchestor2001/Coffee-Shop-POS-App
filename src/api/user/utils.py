import time
import bcrypt
from typing import Union
from jose import JWTError, jwt
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.db import db_helper
from src.settings import settings


class JwtBearer(HTTPBearer):
    SECRET_KEY = settings.token.secret_key
    ALGORITHM = settings.token.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.token.access_token_expire_minutes

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        """
        Handle the JWT authentication request.

        Args:
            request: The HTTP request.

        Returns:
            dict: The decoded JWT payload if valid.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise self.credentials_exception

            # Verify and return the decoded token payload
            token_payload = self.verify_access_token(credentials.credentials)
            if not token_payload:
                raise self.credentials_exception

            return token_payload

        raise self.credentials_exception

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[int, None] = None):
        to_encode = data.copy()
        expire = time.time() + (expires_delta if expires_delta else cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_access_token(cls, token: str) -> Union[dict, None]:
        """
        Verify the JWT token and return the decoded payload.

        Args:
            token: The JWT token to verify.

        Returns:
            dict: The decoded JWT payload if the token is valid.

        Raises:
            HTTPException: If the token is invalid.
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            return None


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def verify_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)


def role_check(allowed_roles: list):
    from src.api.user.crud import get_user_info_obj
    async def check_role(token_payload: dict = Depends(JwtBearer())):
        # Now token_payload contains the decoded JWT data
        async with db_helper.session_factory() as session:
            user_role = (await get_user_info_obj(
                session=session, user_id=token_payload['id']
            )).user_role.value
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"For {user_role} role permission decided")
    return check_role

