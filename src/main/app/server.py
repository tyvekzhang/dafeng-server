import uvicorn
from fastapi import FastAPI

from src.main.app.common.config.config import ServerConfig
from src.main.app.common.config.config_manager import get_server_config
from src.main.app.common.session.db_engine import get_async_engine
from src.main.app.common.session.db_session_middleware import SQLAlchemyMiddleware
from src.main.app.router.router import create_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=get_server_config().name,
    version=get_server_config().version,
    description=get_server_config().app_desc,
    default_response_model_exclude_unset=True,
)


# Register API routes
def register_routes(server_config: ServerConfig) -> None:
    router = create_router()
    app.include_router(router, prefix=server_config.api_version)


# Register essential modules
def register_necessary_modules() -> None:
    import src.main.app.common.exception.exception_handler  # noqa

    app.add_middleware(SQLAlchemyMiddleware, custom_engine=get_async_engine())


# Register optional modules
def register_optional_modules() -> None:
    import src.main.app.common.middleware.jwt_middleware  # noqa
    import src.main.app.common.middleware.cors_middleware  # noqa
    from src.main.app.controller import openapi_controller  # noqa


# Start the Uvicorn server
def start_server(server_config: ServerConfig) -> None:
    app_name="src.main.app.server:app"
    host = server_config.host
    port = server_config.port
    workers = server_config.workers
    uvicorn.run(
        app=app_name,
        host=host,
        port=port,
        workers=workers,
    )


# Main function to run the application
def run() -> None:
    server_config = get_server_config()
    register_routes(server_config)
    register_necessary_modules()
    register_optional_modules()
    start_server(server_config)
