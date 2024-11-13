"""Database domain service interface"""

from abc import ABC, abstractmethod
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.database_model import DatabaseDO


class DatabaseService(ServiceBase[DatabaseDO], ABC):
    @abstractmethod
    async def add(self, *, data: DatabaseDO): ...
