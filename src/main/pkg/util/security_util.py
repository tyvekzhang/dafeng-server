"""Open OAuth2PasswordBearer and provide current user info"""

from datetime import timedelta, datetime
from typing import Any, Union, Callable

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
import jwt
from multipart.exceptions import DecodeError
from passlib.context import CryptContext
from starlette import status

from src.main.pkg.config.config import Config
from src.main.pkg.schema.common_schema import CurrentUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_token(token: str):
    config = Config()
    """Decode JWT and return payload"""
    return jwt.decode(
        token, config.security.secret_key, algorithms=[config.security.algorithm]
    )


def get_user_id(token: str) -> str:
    """Extract user ID from token"""
    payload = decode_token(token)
    return payload["sub"]


def get_current_user() -> Callable[[], CurrentUser]:
    """
    Acquire current info through access_token

    Returns:
        CurrentUser instance
    """
    config = Config()
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl=f"{config.server.api_version}/user/login"
    )

    def current_user(
        access_token: str = Depends(oauth2_scheme),
    ) -> CurrentUser:
        try:
            user_id = get_user_id(access_token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired. Please log in again.",
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error when decoding the token. Please check your request.",
            )

        return CurrentUser(user_id=user_id)

    return current_user


def create_token(
    subject: Union[str, Any],
    expires_delta: Union[timedelta, None] = None,
    token_type: str = None,
) -> str:
    """Create a JWT token"""
    config = Config()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=config.security.access_token_expire_minutes)
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(
        to_encode, config.security.secret_key, algorithm=config.security.algorithm
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def get_payload(token: str):
    """Get payload from token"""
    config = Config()
    return jwt.decode(
        token, config.security.secret_key, algorithms=config.security.algorithm
    )


def is_token_valid(token: str) -> bool:
    """Check if the token is valid"""
    try:
        payload = decode_token(token)
        exp = payload.get("exp")
        return exp and datetime.utcfromtimestamp(exp) > datetime.utcnow()
    except (ExpiredSignatureError, DecodeError):
        return False