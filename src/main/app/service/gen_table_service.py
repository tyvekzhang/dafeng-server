"""GenTable domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.gen_table_schema import TableImport
from src.main.app.service.service_base import ServiceBase


class GenTableService(ServiceBase[GenTableDO], ABC):
    @abstractmethod
    async def import_gen_table(self, data: TableImport):...

