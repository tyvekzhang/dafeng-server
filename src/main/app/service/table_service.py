"""Table domain service interface"""

from abc import ABC
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.table_model import TableDO


class TableService(ServiceBase[TableDO], ABC):
    pass
