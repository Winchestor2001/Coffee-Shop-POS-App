import time
import bcrypt
from typing import Union
from jose import JWTError, jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
        """
        Initialize the JwtBearer class.

        Args:
            auto_error: Whether to raise an exception automatically.
        """
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        """
        Handle the JWT authentication request.

        Args:
            request: The HTTP request.

        Returns:
            str: The JWT token if valid.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise self.credentials_exception

            if not self.verify_access_token(credentials.credentials):
                raise self.credentials_exception

            return credentials.credentials

        raise self.credentials_exception

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[int, None] = None):
        to_encode = data.copy()
        expire = time.time() + (expires_delta if expires_delta else cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_access_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            raise cls.credentials_exception


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def verify_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)

