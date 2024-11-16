from threading import Lock
from typing import Dict, Union

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.model.database_model import DatabaseDO

# Global engine cache with thread safety
_engine_map: Dict[str, AsyncEngine] = {}
_lock = Lock()

from src.main.app.common.config.config_manager import get_database_config

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


async def get_cached_async_engine(
    *, connection_id: Union[str, int] = None, database_id: Union[str, int] = None
) -> AsyncEngine:
    """
    Get or create an AsyncEngine instance based on the URL.
    Uses thread-safe singleton pattern to cache engines.

    Args:
        connection_id: Database connection id.
        database_id: Database id.

    Returns:
        AsyncEngine: SQLAlchemy async engine instance
    """
    global _engine_map

    cache_key = str(connection_id) + str(database_id)
    # Get database config
    database_config = get_database_config()

    # Return cached engine if exists
    with _lock:
        if cache_key in _engine_map:
            return _engine_map[cache_key]
        database: DatabaseDO = await databaseMapper.select_by_id(id=database_id)
        if database is not None:
            connection_id = database.connection_id
        connection: ConnectionDO = await connectionMapper.select_by_id(id=connection_id)
        if connection is None:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code, ResponseCode.PARAMETER_ERROR.msg
            )

        database_type = connection.database_type
        host = connection.host
        port = connection.port
        username = connection.username
        password = connection.password
        database_type = database_type.lower()
        if database_type == "mysql":
            url = f"mysql+aiomysql://{username}:{password}@{host}:{port}"
        elif database_type == "postgresql":
            url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}"
        elif database_type == "sqlite":
            url = "sqlite+aiosqlite:///~/df.db"
        else:
            raise SystemException(
                ResponseCode.UNSUPPORTED_DIALECT_ERROR.code,
                f"{ResponseCode.UNSUPPORTED_DIALECT_ERROR.msg}: {database_type}",
            )
        if database is not None:
            url = str(url) + "/" + database.database_name

        # Create new engine if not cached
        new_engine = create_async_engine(
            url=url,
            echo=database_config.echo_sql,
            pool_recycle=database_config.pool_recycle,
        )

        # Cache the new engine
        _engine_map[cache_key] = new_engine
        return new_engine


async def clear_engine_cache() -> None:
    """
    Clear all cached engine instances.
    Should be called when shutting down the application.
    """
    global _engine_map
    with _lock:
        for engine in _engine_map.values():
            await engine.dispose()
        _engine_map.clear()
