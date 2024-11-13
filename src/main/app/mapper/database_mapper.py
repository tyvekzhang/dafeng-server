"""Database mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.database_model import DatabaseDO


class DatabaseMapper(SqlModelMapper[DatabaseDO]):
    pass


databaseMapper = DatabaseMapper(DatabaseDO)
