"""Database domain service impl"""

from sqlmodel import text

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.mapper.database_mapper import DatabaseMapper
from src.main.app.model.database_model import DatabaseDO
from src.main.app.schema.database_schema import DB_CREATE_TEMPLATES
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

    async def add(self, *, data: DatabaseDO):
        engine = await get_cached_async_engine(connection_id=data.connection_id)
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
        await self.mapper.insert(record=data)
