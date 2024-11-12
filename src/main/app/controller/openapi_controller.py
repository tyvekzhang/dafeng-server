import os

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from src.main.app.common.config.config_manager import get_server_config
from src.main.app.server import app


def get_static_dir() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    static_dir = os.path.join(base_dir, "common/static")
    return static_dir


app.mount("/static", StaticFiles(directory=get_static_dir()), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        swagger_favicon_url="/static/favicon.png",
        openapi_url=app.openapi_url,
        title=get_server_config().name,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        redoc_favicon_url="/static/favicon.png",
        openapi_url=app.openapi_url,
        title=get_server_config().name,
        redoc_js_url="/static/redoc.standalone.js",
    )
