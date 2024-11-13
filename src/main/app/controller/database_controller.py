from typing import Dict, Optional

from fastapi import APIRouter
from sqlmodel import inspect, text

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common import result
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.model.database_model import DatabaseDO
from src.main.app.schema.database_schema import DatabaseAdd
from src.main.app.service.database_service import DatabaseService
from src.main.app.service.impl.database_service_impl import DatabaseServiceImpl

database_router = APIRouter()
database_service: DatabaseService = DatabaseServiceImpl(mapper=databaseMapper)


@database_router.post("/add")
async def add_database(data: DatabaseAdd):
    record = DatabaseDO(**data.model_dump())
    await database_service.add(data=record)
    return result.success()


@database_router.get("/version")
async def get_database_version(connection_id: Optional[int] = None) -> Dict:
    engine = await get_cached_async_engine(connection_id=connection_id)
    async with engine.connect() as conn:
        dialect_name = engine.dialect.name.lower()
        if dialect_name == "sqlite":
            version_info = await conn.execute(text("SELECT sqlite_version();"))
        elif dialect_name in ("mysql", "mariadb"):
            version_info = await conn.execute(text("SELECT VERSION();"))
        elif dialect_name == "postgresql":
            version_info = await conn.execute(text("SELECT version();"))
        else:
            raise SystemException(
                ResponseCode.DB_UNKNOWN_ERROR.code,
                f"Unknown database dialect: {dialect_name}. "
                + ResponseCode.DB_UNKNOWN_ERROR.msg,
            )
        version = str((version_info.fetchone())[0]).split("-")[0]
    return result.success({"version_schema": f"{dialect_name}:{version}"})


@database_router.get("/tables")
async def get_tables(database_id: Optional[int] = None) -> Dict:
    engine = await get_cached_async_engine(database_id=database_id)
    async with engine.connect() as conn:
        table_names = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    table_info = []

    for table in table_names:
        if table == "alembic_version":
            continue
        if engine.dialect.name == "sqlite":
            table_info.append({"table_name": table, "comment": table})
            continue
        async with engine.connect() as conn:
            table_comment = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_comment(table)
            )

        table_info.append(
            {
                "table_name": table,
                "comment": table_comment.get("text", "") if table_comment else "",
            }
        )

    return result.success(table_info)


@database_router.get("/{database_id}/{table_name}/info")
async def get_table_fields(table_name: str, database_id: int) -> Dict:
    engine = await get_cached_async_engine(database_id=database_id)
    async with engine.connect() as conn:
        dialect_name = engine.dialect.name.lower()
        columns = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_columns(table_name)
        )
        if dialect_name != "sqlite":
            table_options = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_options(table_name)
            )
        else:
            table_options = {}
        indexes = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_indexes(table_name)
        )
    indexed_columns = set()
    for index in indexes:
        for col in index["column_names"]:
            indexed_columns.add(col)
    fields = []
    for column in columns:
        fields.append(
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "indexed": column["name"] in indexed_columns,
                "comment": column.get("comment", column["name"]),
            }
        )
    all_indexes = []
    for index in indexes:
        unique = index.get("unique", False)
        if unique == 0:
            unique = False
        elif unique == 1:
            unique = True
        all_indexes.append(
            {
                "name": index["name"],
                "column_names": index["column_names"],
                "unique": unique,
            }
        )
    return result.success(
        {
            "table": table_name,
            "fields": fields,
            "table_options": table_options,
            "indexes": all_indexes,
        }
    )
