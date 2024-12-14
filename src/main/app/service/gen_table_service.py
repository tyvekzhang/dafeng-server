"""GenTable domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.gen_table_schema import TableImport, GenTableQuery
from src.main.app.service.service_base import ServiceBase


class GenTableService(ServiceBase[GenTableDO], ABC):
    @abstractmethod
    async def import_gen_table(self, data: TableImport):...

    @abstractmethod
    async def preview_code(self, table_id: int):...

    @abstractmethod
    async def list_gen_tables(self, data: GenTableQuery):...

    @abstractmethod
    async def download_code(self, table_id: int):...
