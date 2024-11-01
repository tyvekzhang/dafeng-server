"""User domain schema"""

import re
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlmodel import Field

from src.main.pkg.type.user_do import UserDO


class RefreshToken(BaseModel):
    """
    RefreshToken schema
    """

    refresh_token: str


class UserCreateCmd(BaseModel):
    """
    UserCreate schema
    """

    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=6, max_length=32)
    nickname: str = Field(..., min_length=2, max_length=32)
    remark: Optional[str] =  Field("",  max_length=255)

    @field_validator("password")
    def password_complexity(cls, value):
        """
        Validate password strength:
        - Contains an uppercase letter
        - Contains a lowercase letter
        - Contains a digit
        """
        if not re.search(r"^(?=.*[a-zA-Z])(?=.*\d).+$", value):
            raise ValueError("Password must contain digit and letter")
        return value


class LoginCmd(BaseModel):
    """
    Login schema
    """

    username: str
    password: str


class UserQuery(UserDO):
    """
    UserQuery schema
    """
    pass

class UserUpdateCmd(BaseModel):
    id: int
    nickname: Optional[str] = None
    status:  Optional[int] = None
    remark: Optional[str] = None
