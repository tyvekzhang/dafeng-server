"""Index domain service impl"""

from src.main.app.mapper.index_mapper import IndexMapper
from src.main.app.model.db_index_model import IndexDO
from src.main.app.schema.index_schema import IndexQuery
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.index_service import IndexService


class IndexServiceImpl(ServiceBaseImpl[IndexMapper, IndexDO], IndexService):
    def __init__(self, mapper: IndexMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_indexes(self, data: IndexQuery):
        return await self.mapper.select_ordered_pagination(
            page=data.current,
            size=data.pageSize,
            order_by=data.order_by,
            sort_order=data.sort_order,
            count=data.count,
            filter_by={"table_id": data.table_id},
        )
