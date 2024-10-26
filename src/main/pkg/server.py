from argparse import Namespace
import uvicorn
from fastapi import FastAPI

from src.main.pkg.io.config import Config, load_config
from src.main.pkg.router.router import create_router
from src.main.pkg.session.db_session_middleware import SQLAlchemyMiddleware

app = FastAPI()

def register_routes(api_version: str) -> None:
    router = create_router()
    app.include_router(router, prefix=api_version)


def register_exception_handler() -> None:
    from src.main.pkg.exception import exception_handler  # noqa


def register_middleware(config: Config) -> None:
    db_config = config.database
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=str(db_config.url),
        engine_args={
            "echo": db_config.echo_sql,
            "pool_recycle": db_config.pool_recycle,
        },
    )


def start_server(config: Config) -> None:
    server_config = config.server
    register_routes(server_config.api_version)
    register_exception_handler()
    register_middleware(config)
    uvicorn.run(
        app=app,
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
    )


def run(args: Namespace) -> None:
    config: Config = load_config(args)
    start_server(config)
