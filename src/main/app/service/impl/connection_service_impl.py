"""Connection domain service impl"""

from src.main.app.common.config.config_manager import (
    load_config,
)
from src.main.app.common.exception.exception import SystemException
from src.main.app.mapper.connection_mapper import ConnectionMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.schema.connection_schema import (
    ConnectionQuery,
    ConnectionQueryResponse,
)
from src.main.app.service.connection_service import ConnectionService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class ConnectionServiceImpl(ServiceBaseImpl[ConnectionMapper, ConnectionDO], ConnectionService):
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

    async def list_connections(self, data: ConnectionQuery):
        records, total_count = await self.mapper.select_ordered_pagination(
            page=data.page,
            size=data.size,
            sort_order=data.sort_order,
            order_by=data.order_by,
            count=data.count,
        )
        if total_count == 0:
            database_config = load_config().database
            dialect = database_config.dialect
            url = database_config.url
            connection_do: ConnectionDO
            if dialect.lower() == "sqlite" or dialect.lower() == "postgresql":
                raise SystemException(-1, "Not support yet")

            # driver://user:pass@localhost:port/dbname
            url = url.split("//")[1]
            user_pass_arr = url.split("@")[0].split(":")
            host_port_arr = url.split("@")[1].split("/")[0].split(":")
            host = host_port_arr[0]
            port = host_port_arr[1]
            username = user_pass_arr[0]
            password = user_pass_arr[1]
            connection_do = ConnectionDO(
                connection_name="默认",
                database_type=dialect,
                host=host,
                port=port,
                username=username,
                password=password,
            )
            await self.mapper.insert(record=connection_do)
            return [connection_do], 1
        records = [ConnectionQueryResponse(**record.model_dump()) for record in records]
        return records, total_count
