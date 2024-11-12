"""Connection domain service interface"""

from abc import ABC
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.connection_model import ConnectionDO


class ConnectionService(ServiceBase[ConnectionDO], ABC):
    pass
