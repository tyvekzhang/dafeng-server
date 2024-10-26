from argparse import Namespace
import uvicorn
from fastapi import FastAPI

from src.main.pkg.io.config import Config
from src.main.pkg.io.config_loader import ConfigLoader
from src.main.pkg.router.router import create_router

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)


def load_config(args: Namespace) -> Config:
    env = args.env

    config_file = args.config_file
    config_loader = ConfigLoader(env, config_file)
    config = config_loader.load_config()

    return Config(config)


def register_routes(api_version: str) -> None:
    router = create_router()
    app.include_router(router, prefix=api_version)


def register_exception_handler() -> None:
    from src.main.pkg.exception import exception_handler  # noqa


def start_server(config: Config) -> None:
    server = config.server
    register_routes(server.api_version)
    register_exception_handler()
    uvicorn.run(app=app, host=server.host, port=server.port, workers=server.workers)


def run(args: Namespace) -> None:
    config: Config = load_config(args)
    start_server(config)
