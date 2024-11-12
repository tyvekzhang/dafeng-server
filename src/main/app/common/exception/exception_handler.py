"""Global exception handler"""

import http

from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from pydantic_core._pydantic_core import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse, Response
from jwt import PyJWTError

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import ServiceException
from src.main.app.server import app


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Asynchronous exception handler for all unhandled exceptions.

    Args:
        request (Request): The request instance containing all request details.
        exc (Exception): The exception instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)
    return JSONResponse(
        {"code": ResponseCode.SERVICE_INTERNAL_ERROR.code, "msg": str(exc)},
        status_code=status_code,
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Asynchronous exception handler for validation exceptions.

    Args:
        request (Request): The request instance containing all request details.
        exc (ValidationError): The exception instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)
    return JSONResponse(
        {
            "code": ResponseCode.SERVICE_INTERNAL_ERROR.code,
            "msg": str(exc).split("For further")[0],
        },
        status_code=status_code,
    )


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """
    Asynchronous handler for ServiceException.

    Args:
        request (Request): The request instance containing all request details.
        exc (ServiceException): The ServiceException instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {"code": exc.code, "msg": exc.msg},
        status_code=exc.status_code,
        headers=headers,
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Asynchronous handler for StarletteHTTPException.

    Args:
        request (Request): The request instance containing all request details.
        exc (StarletteHTTPException): The StarletteHTTPException instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Asynchronous handler for RequestValidationError.

    Args:
        request (Request): The request instance containing all request details.
        exc (RequestValidationError): The RequestValidationError instance.

    Returns:
        Response: A JSONResponse object which contain code and msg,
    """
    return JSONResponse(
        {"code": http.HTTPStatus.UNPROCESSABLE_ENTITY, "msg": str(exc.errors())},
    )


@app.exception_handler(PyJWTError)
async def jwt_exception_handler() -> JSONResponse:
    """
    Asynchronous handler for JWT-related exceptions.

    Args:
        request (Request): The request instance containing all request details.
        exc (PyJWTError): The JWTError instance indicating the error.

    Returns:
        JSONResponse: A JSON response with an error code and message.
    """
    return JSONResponse(
        status_code=http.HTTPStatus.UNAUTHORIZED,
        content={
            "code": http.HTTPStatus.UNAUTHORIZED,
            "msg": "Your token has expired. Please log in again.",
        },
    )
