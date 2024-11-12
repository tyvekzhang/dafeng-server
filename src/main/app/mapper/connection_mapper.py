"""Connection mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.connection_model import ConnectionDO


class ConnectionMapper(SqlModelMapper[ConnectionDO]):
    pass


connectionMapper = ConnectionMapper(ConnectionDO)
