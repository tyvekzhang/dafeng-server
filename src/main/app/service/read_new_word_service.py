"""NewWord domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.read_new_word_schema import NewWordQuery
from src.main.app.service.service_base import ServiceBase


class NewWordService(ServiceBase[NewWordDO], ABC):

    @abstractmethod
    async def fetch_new_word_by_page(self, new_word_query: NewWordQuery):
        pass
