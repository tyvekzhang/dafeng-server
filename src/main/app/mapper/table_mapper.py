"""Table mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.table_model import TableDO


class TableMapper(SqlModelMapper[TableDO]):
    pass


tableMapper = TableMapper(TableDO)
