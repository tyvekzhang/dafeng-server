"""Table domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.schema.table_schema import TableQuery, TableGenerate
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.table_model import TableDO


class TableService(ServiceBase[TableDO], ABC):
    @abstractmethod
    async def list_tables(self, data: TableQuery): ...

    @abstractmethod
    async def generate_table(self, table_generate: TableGenerate) -> None: ...
