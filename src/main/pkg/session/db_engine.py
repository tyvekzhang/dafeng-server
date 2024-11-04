from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.main.pkg.config.config_manager import get_database_config

async_engine: AsyncEngine


def get_async_engine():
    global async_engine
    database_config = get_database_config()
    async_engine = create_async_engine(
        url=database_config.url,
        echo=database_config.echo_sql,
        pool_recycle=database_config.pool_recycle,
    )
    return async_engine
