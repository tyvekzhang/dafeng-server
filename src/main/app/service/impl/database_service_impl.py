"""Database domain service impl"""

from typing import Tuple, List, Any

from sqlmodel import text

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException, ParameterException
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.mapper.database_mapper import DatabaseMapper
from src.main.app.model.db_database_model import DatabaseDO
from src.main.app.schema.database_schema import (
    DB_CREATE_TEMPLATES,
    DatabaseQuery,
    DatabaseAdd,
    SQLSchema,
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
                    encoding=data.encoding,
                    collation_order=data.collation_order,
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
        connection_record = await connectionMapper.select_by_id(id=connection_id)
        if connection_record is None:
            raise ParameterException()
        engine = await get_cached_async_engine(connection_id=connection_id)
        async with engine.connect() as conn:
            # 获取数据库的 dialect 类型
            dialect_name = conn.dialect.name.lower()

            if dialect_name == 'mysql':
                # MySQL 查询
                query = """
                    SELECT SCHEMA_NAME database_name,
                           DEFAULT_CHARACTER_SET_NAME encoding,
                           DEFAULT_COLLATION_NAME collation_order
                      FROM information_schema.SCHEMATA
                """
                query_response = await conn.execute(text(query))
                rows = query_response.mappings().fetchall()
                # 将结果转换为 MySQLSchema 对象
                database_records = [SQLSchema(**row) for row in rows]

            elif dialect_name == 'sqlite':
                # SQLite 查询 - 获取数据库中的所有表
                query = "SELECT name FROM sqlite_master WHERE type='table'"
                query_response = await conn.execute(text(query))
                rows = query_response.mappings().fetchall()
                # SQLite 没有 schema 概念，但可以返回数据库中的表名作为 schema 名字
                database_records = [SQLSchema(database_name=row['name']) for row in rows]

            elif dialect_name == 'postgresql':
                # PostgreSQL 查询
                query = """
                    SELECT
                        datname AS database_name,
                        pg_catalog.pg_get_userbyid(datdba) AS owner,
                        (SELECT datname FROM pg_database WHERE oid = dattablespace) AS template,
                        pg_encoding_to_char(encoding) AS encoding,
                        datcollate AS collation_order,
                        datctype AS character_classification,
                        spcname AS tablespace,
                        datconnlimit AS connection_limit,
                        datallowconn AS allow_connection,
                        datistemplate AS is_template
                    FROM
                        pg_database d
                    LEFT JOIN
                        pg_tablespace t ON d.dattablespace = t.oid;
                """
                query_response = await conn.execute(text(query))
                rows = query_response.mappings().fetchall()
                # 将结果转换为 PostgreSQLSchema 对象
                database_records = [SQLSchema(**row) for row in rows]

            else:
                raise ValueError(f"Unsupported database dialect: {dialect_name}")
        new_add_databases = []
        need_delete_ids = []
        records: List[DatabaseDO] = await self.mapper.select_by_connection_id(connection_id=connection_id)
        exist_database_names = set()
        if records is not None:
            exist_database_names = {record.database_name: record.id for record in records}
        for record in database_records:
            if record.database_name not in exist_database_names:
                new_add_databases.append(
                    DatabaseDO(
                        **DatabaseAdd(
                            connection_id=connection_id,
                            database_name=record.database_name,
                            encoding=record.encoding,
                            collation_order=record.collation_order,
                        ).model_dump()
                    )
                )
        database_names = [record.database_name for record in database_records]
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
