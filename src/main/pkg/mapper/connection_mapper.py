"""Connection mapper"""

from src.main.pkg.mapper.mapper_base_impl import SqlModelMapper
from src.main.pkg.model.connection_model import ConnectionDO


class ConnectionMapper(SqlModelMapper[ConnectionDO]):
    pass


connectionMapper = ConnectionMapper(ConnectionDO)
