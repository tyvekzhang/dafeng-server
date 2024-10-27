import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.main.pkg.config.config import Config
from src.main.pkg.router.router import create_router
from src.main.pkg.session.db_session_middleware import SQLAlchemyMiddleware

config = Config()
server = config.server
security = config.security

app = FastAPI(
    title=server.name,
    version=server.version,
    openapi_url=f"{server.api_version}/openapi.json",
    description=server.app_desc,
    default_response_model_exclude_unset=True,
)

origins = [origin.strip() for origin in security.backend_cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def register_routes(api_version: str) -> None:
    router = create_router()
    app.include_router(router, prefix=api_version)


def register_necessary_modules(c: Config) -> None:
    import src.main.pkg.plugin.exception_handler  # noqa

    db_config = c.database
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=str(db_config.url),
        engine_args={
            "echo": db_config.echo_sql,
            "pool_recycle": db_config.pool_recycle,
        },
    )


def register_optional_modules() -> None:
    import src.main.pkg.plugin.jwt_middleware  # noqa


def run(c: Config) -> None:
    server_config = c.server
    register_routes(server_config.api_version)
    register_necessary_modules(c)
    register_optional_modules()
    uvicorn.run(
        app=app,
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
    )
