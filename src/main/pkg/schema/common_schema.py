"""Common schema"""
from typing import Optional, Dict, Any

from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema
    """

    access_token: str
    token_type: str
    expired_at: int
    refresh_token: str
    re_expired_at: int


class CurrentUser(BaseModel):
    """
    CurrentUser schema
    """

    id: int


class BasePage(BaseModel):
    """
    Paging schema
    """

    page: Optional[int] = 1
    size: Optional[int] = 10
    count: Optional[bool] = True

class FilterParams(BasePage):
    """
    UserFilterParams schema
    """

    filter_by: Optional[Dict[str, Any]] = None
    like: Optional[Dict[str, str]] = None

class BaseParams(BaseModel):
    """
    BaseParams for all data object
    """
    id: int
    create_time: int
    update_time: Optional[int] = None