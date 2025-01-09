"""GenTableField domain service interface"""

from abc import ABC

from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.service.service_base import ServiceBase


class GenTableFieldService(ServiceBase[GenFieldDO], ABC):
    pass
