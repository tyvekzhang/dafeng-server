"""GenTable domain service impl"""
from typing import List

from sqlmodel import inspect

from src.main.app.common.gen.gen_util import GenUtils
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.common.util.string_util import StringUtils
from src.main.app.mapper.field_mapper import fieldMapper
from src.main.app.mapper.gen_field_mapper import genFieldMapper
from src.main.app.mapper.gen_table_mapper import GenTableMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_table_model import TableDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.gen_table_schema import TableImport
from src.main.app.service.gen_table_service import GenTableService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class GenTableServiceImpl(ServiceBaseImpl[GenTableMapper, GenTableDO], GenTableService):
    def __init__(self, mapper: GenTableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def import_gen_table(self, data: TableImport):
        database_id = data.database_id
        table_ids = data.table_ids
        table_records: List[TableDO] = await tableMapper.select_by_ids(ids=table_ids)
        engine = await get_cached_async_engine(database_id=database_id)
        async with engine.connect() as conn:
            try:
                for table_record in table_records:
                    table_name = table_record.name
                    comment = table_record.comment
                    if comment is None:
                        comment = "[请填写功能名]"
                    table_id = table_record.id
                    gen_table_data = GenTableDO(db_table_id=table_id, class_name = table_name, function_name = comment)
                    GenUtils.init_table(gen_table_data)
                    await self.save(data=gen_table_data)
                    field_records = await fieldMapper.select_by_table_id(table_id=table_id)
                    for field_record in field_records:
                        gen_field = GenFieldDO(db_field_id=field_record.id)
                        GenUtils.init_field(gen_field, field_record)
                        await genFieldMapper.insert(record=gen_field)

                    # columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns(table_name))
                    #
                    # indexes = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_indexes(table_name))
                    # pk_index = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_pk_constraint(table_name))
            except Exception as e:
                print(e)
                columns = []
                indexes = []
                pk_index = []