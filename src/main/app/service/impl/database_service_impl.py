"""Database domain service impl"""

from typing import Tuple, List, Any

from sqlmodel import text

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.mapper.database_mapper import DatabaseMapper
from src.main.app.model.db_database_model import DatabaseDO
from src.main.app.schema.database_schema import (
    DB_CREATE_TEMPLATES,
    DatabaseQuery,
    DatabaseAdd,
    MySQLSchema,
)
from src.main.app.service.database_service import DatabaseService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class DatabaseServiceImpl(ServiceBaseImpl[DatabaseMapper, DatabaseDO], DatabaseService):
    """
    Implementation of the DatabaseService interface.
    """

    def __init__(self, mapper: DatabaseMapper):
        """
        Initialize the DatabaseServiceImpl instance.

        Args:
            mapper (DatabaseMapper): The DatabaseMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def add(self, *, data: DatabaseDO) -> DatabaseDO:
        engine = await get_cached_async_engine(connection_id=data.connection_id)
        database = await self.mapper.insert(record=data)
        async with engine.connect() as conn:
            # Get database type
            dialect_name = engine.dialect.name.lower()

            # Check if db exists for MySQL
            if dialect_name == "mysql":
                db_result = await conn.execute(
                    text(
                        f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{data.database_name}'"
                    )
                )
                if db_result.fetchone():
                    raise SystemException(
                        ResponseCode.DATABASE_ALREADY_EXIST.code,
                        f"{ResponseCode.DATABASE_ALREADY_EXIST.msg}: {data.database_name}",
                    )

            # Execute create SQL
            if dialect_name in DB_CREATE_TEMPLATES:
                create_sql = DB_CREATE_TEMPLATES[dialect_name].format(
                    database_name=data.database_name,
                    character_set=data.character_set,
                    collation=data.collation,
                )

                if dialect_name != "sqlite":
                    await conn.execute(text("COMMIT;"))
                    await conn.execute(text(create_sql))
                    await conn.commit()

            else:
                raise SystemException(
                    ResponseCode.UNSUPPORTED_DIALECT_ERROR.code,
                    f"{ResponseCode.UNSUPPORTED_DIALECT_ERROR.msg}: {dialect_name}",
                )
        return database

    async def list_databases(self, data: DatabaseQuery) -> Tuple[List[Any], int]:
        connection_id = data.connection_id
        engine = await get_cached_async_engine(connection_id=connection_id)
        async with engine.connect() as conn:
            query = "select SCHEMA_NAME schema_name, DEFAULT_CHARACTER_SET_NAME default_character_set_name, DEFAULT_COLLATION_NAME default_collation_name FROM information_schema.SCHEMATA"
            query_response = await conn.execute(text(query))
            rows = query_response.mappings().fetchall()
            database_records = [MySQLSchema(**row) for row in rows]
        new_add_databases = []
        need_delete_ids = []
        records: List[DatabaseDO] = await self.mapper.select_by_connection_id(connection_id=connection_id)
        exist_database_names = set()
        if records is not None:
            exist_database_names = {record.database_name: record.id for record in records}
        for record in database_records:
            if record.schema_name not in exist_database_names:
                new_add_databases.append(
                    DatabaseDO(
                        **DatabaseAdd(
                            connection_id=connection_id,
                            database_name=record.schema_name,
                            character_set=record.default_character_set_name,
                            collation=record.default_collation_name,
                        ).model_dump()
                    )
                )
        database_names = [record.schema_name for record in database_records]
        for database_name in exist_database_names.keys():
            if database_name not in set(database_names):
                need_delete_ids.append(exist_database_names[database_name])
        if len(new_add_databases) > 0:
            await self.mapper.batch_insert(records=new_add_databases)
        if len(need_delete_ids) > 0:
            await self.mapper.batch_delete_by_ids(ids=need_delete_ids)
        return await self.mapper.select_ordered_pagination(
            page=data.page,
            size=data.size,
            order_by=data.order_by,
            sort_order=data.sort_order,
            count=data.count,
            filter_by={"connection_id": connection_id},
        )
