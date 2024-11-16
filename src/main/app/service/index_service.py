"""Index domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.schema.index_schema import IndexQuery
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.index_model import IndexDO


class IndexService(ServiceBase[IndexDO], ABC):
    @abstractmethod
    async def list_indexes(self, data: IndexQuery): ...
