"""Connection domain service impl"""

from src.main.app.mapper.connection_mapper import ConnectionMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.service.connection_service import ConnectionService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class ConnectionServiceImpl(
    ServiceBaseImpl[ConnectionMapper, ConnectionDO], ConnectionService
):
    """
    Implementation of the ConnectionService interface.
    """

    def __init__(self, mapper: ConnectionMapper):
        """
        Initialize the ConnectionServiceImpl instance.

        Args:
            mapper (ConnectionMapper): The ConnectionMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper
