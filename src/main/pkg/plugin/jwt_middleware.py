"""Jwt middleware"""

import http

from fastapi import Request
from loguru import logger
from starlette.responses import JSONResponse

from src.main.pkg.config.config import Config
from src.main.pkg.server import app
from src.main.pkg.util.security_util import is_token_valid


@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    configs = Config()
    security = configs.security
    if not security.enable:
        return await call_next(request)
    api_version = configs.server.api_version
    raw_url_path = request.url.path
    if not raw_url_path.__contains__(api_version) or raw_url_path.__contains__(".json"):
        if security.enable_swagger:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=http.HTTPStatus.FORBIDDEN,
                content={"detail": "The documentation isn't ready yet."},
            )
    white_list_routes = [
        router.strip() for router in security.white_list_routes.split(",")
    ]
    request_url_path = api_version + raw_url_path.split(api_version)[1]
    if request_url_path in white_list_routes:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            is_token_valid(token)
        except Exception as e:
            logger.error(f"{e}")
            return JSONResponse(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                content={"detail": "Invalid token or expired token"},
            )

    else:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Authentication token"},
        )

    return await call_next(request)