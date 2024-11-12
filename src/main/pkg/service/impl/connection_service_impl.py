"""Connection domain service impl"""

from src.main.pkg.mapper.connection_mapper import ConnectionMapper
from src.main.pkg.model.connection_model import ConnectionDO
from src.main.pkg.service.connection_service import ConnectionService
from src.main.pkg.service.impl.service_base_impl import ServiceBaseImpl


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
