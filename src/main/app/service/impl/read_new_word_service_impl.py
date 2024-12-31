"""NewWord domain service impl"""
import random
from random import randint

from src.main.app.common.config.config_manager import (
    load_config,
)
from src.main.app.common.exception.exception import SystemException
from src.main.app.mapper.read_new_word_mapper import NewWordMapper
from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.read_new_word_schema import NewWordQuery, NewWordQueryResponse
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.read_new_word_service import NewWordService


class NewWordServiceImpl(ServiceBaseImpl[NewWordMapper, NewWordDO], NewWordService):
    """
    Implementation of the NewWordService interface.
    """

    def __init__(self, mapper: NewWordMapper):
        """
        Initialize the NewWordServiceImpl instance.

        Args:
            mapper (NewWordMapper): The NewWordMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_new_word_by_page(self, new_word_query: NewWordQuery):
        filter_by = {}
        if new_word_query.word is not None and new_word_query.word != "":
            filter_by={"word": new_word_query.word}
        records, total_count = await self.mapper.select_ordered_pagination(
            page=new_word_query.current,
            size=new_word_query.pageSize,
            filter_by=filter_by,
            count=True,
        )
        records = [NewWordQueryResponse(id=record.id, word=record.word) for record in records]
        return records, total_count
