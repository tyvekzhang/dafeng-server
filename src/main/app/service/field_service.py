"""Field domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.schema.field_schema import FieldQuery
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.field_model import FieldDO


class FieldService(ServiceBase[FieldDO], ABC):
    @abstractmethod
    async def list_fields(self, data: FieldQuery): ...