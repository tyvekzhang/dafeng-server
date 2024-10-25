from typing import Generic, TypeVar, Optional, Dict

from pydantic import BaseModel

# Define generic type variables
DataType = TypeVar("DataType")
T = TypeVar("T")

# Define default response codes and messages
DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_FAIL_CODE: int = -1
DEFAULT_SUCCESS_MSG: str = "success"


class BaseResponse(BaseModel, Generic[T]):
    """
    Base response model for API responses.

    Attributes:
        msg: Response message
        code: Response status code
        data: Optional response data of generic type T
    """

    msg: str = DEFAULT_SUCCESS_MSG
    code: Optional[int] = DEFAULT_SUCCESS_CODE
    data: Optional[T] = None


def success(
    data: DataType = None,
    msg: Optional[str] = DEFAULT_SUCCESS_MSG,
    code: Optional[int] = DEFAULT_SUCCESS_CODE,
) -> Dict:
    """
    Generate a success response dictionary

    Args:
        data: Response data of generic type DataType
        msg: Success message
        code: Success status code

    Returns:
        Dict containing response data
    """
    if data is None:
        return {"code": code, "msg": msg}
    return {"code": code, "msg": msg, "data": data}


def fail(msg: str, code: int = DEFAULT_FAIL_CODE) -> Dict:
    """
    Generate a failure response dictionary

    Args:
        msg: Error message
        code: Error status code

    Returns:
        Dict containing error response
    """
    return {"code": code, "msg": msg}
