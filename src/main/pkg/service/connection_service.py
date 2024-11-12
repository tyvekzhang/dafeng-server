"""Connection domain service interface"""

from abc import ABC
from src.main.pkg.service.service_base import ServiceBase
from src.main.pkg.model.connection_model import ConnectionDO


class ConnectionService(ServiceBase[ConnectionDO], ABC):
    pass
