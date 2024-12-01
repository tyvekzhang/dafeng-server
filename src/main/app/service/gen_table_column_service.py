"""GenTableColumn domain service interface"""

from abc import ABC

from src.main.app.model.gen_table_field_model import GenTableColumnDO
from src.main.app.service.service_base import ServiceBase


class GenTableColumnService(ServiceBase[GenTableColumnDO], ABC):
    pass
