from threading import Lock
from typing import Dict, Union

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from sqlmodel import select
from src.main.app.common.config.config_manager import get_database_config
from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common.session.db_session import db_session
from src.main.app.common.util.work_path_util import db_path
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.model.database_model import DatabaseDO

# Global engine cache with thread safety
_engine_map: Dict[str, AsyncEngine] = {}
_lock = Lock()

async_engine: AsyncEngine


def get_async_engine():
    global async_engine
    database_config = get_database_config()
    async_engine = create_async_engine(
        url=database_config.url,
        echo=database_config.echo_sql,
        pool_size=database_config.pool_size,
        max_overflow=database_config.max_overflow,
        pool_recycle=database_config.pool_recycle,
        pool_pre_ping=True,
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

        url = get_database_url(database, connection)

        # Create new engine if not cached
        new_engine = create_async_engine(url=url, poolclass=NullPool)

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


async def get_engine_by_database_id(*, env: str, database_id: int):
    async with db_session(env=env) as session:
        statement = select(DatabaseDO).where(DatabaseDO.id == database_id)
        exec_response = await session.exec(statement)
        database: DatabaseDO = exec_response.one_or_none()
        if database is None:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code, ResponseCode.PARAMETER_ERROR.msg
            )
        statement = select(ConnectionDO).where(
            ConnectionDO.id == database.connection_id
        )
        exec_response = await session.exec(statement)
        connection: ConnectionDO = exec_response.one_or_none()
        if connection is None:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code, ResponseCode.PARAMETER_ERROR.msg
            )
        url = get_database_url(database, connection)
        engine = create_async_engine(
            url=url,
        )
        return engine


def get_database_url(database: DatabaseDO, connection: ConnectionDO) -> str:
    database_type = connection.database_type
    database_type = database_type.lower()
    if database_type == "sqlite":
        url = f"sqlite+aiosqlite:///{db_path}"
    elif database_type == "mysql":
        host = connection.host
        port = connection.port
        username = connection.username
        password = connection.password
        url = f"mysql+aiomysql://{username}:{password}@{host}:{port}"
        if database is not None:
            url = str(url) + "/" + database.database_name
    else:
        raise SystemException(
            ResponseCode.UNSUPPORTED_DIALECT_ERROR.code,
            f"{ResponseCode.UNSUPPORTED_DIALECT_ERROR.msg}: {database_type}",
        )
    return url
