"""Database domain service interface"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Any

from src.main.app.schema.database_schema import DatabaseQuery
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.database_model import DatabaseDO


class DatabaseService(ServiceBase[DatabaseDO], ABC):
    @abstractmethod
    async def add(self, *, data: DatabaseDO) -> DatabaseDO: ...

    @abstractmethod
    async def list_databases(self, data: DatabaseQuery) -> Tuple[List[Any], int]: ...
