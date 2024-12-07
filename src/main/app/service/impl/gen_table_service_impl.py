"""GenTable domain service impl"""
from collections import OrderedDict
from typing import List, Dict

from sqlmodel import inspect

from src.main.app.common.exception.exception import ParameterException
from src.main.app.common.gen.gen_util import GenUtils
from src.main.app.common.gen.jinja2_util import Jinja2Utils
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.common.util.string_util import StringUtils
from src.main.app.common.util.template_util import load_template_file
from src.main.app.mapper.field_mapper import fieldMapper
from src.main.app.mapper.gen_field_mapper import genFieldMapper
from src.main.app.mapper.gen_table_mapper import GenTableMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_table_model import TableDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.gen_field_schema import FieldGen
from src.main.app.schema.gen_table_schema import TableImport, TableGen
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
                    gen_table_data = GenTableDO(db_table_id=table_id, class_name = table_name, function_name = comment, table_name=table_record.name)
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

    async def preview_code(self, table_id: int) -> Dict:
        data_map = OrderedDict()
        # 查询导入的表信息
        gen_table: GenTableDO = await self.retrieve_by_id(id=table_id)
        if gen_table is None:
            raise ParameterException()
        self.set_sub_table(gen_table=gen_table)
        self.set_pk_column(gen_table=gen_table)
        # 通过表id查询父字段信息
        field_records = await fieldMapper.select_by_table_id(table_id=gen_table.db_table_id)
        if field_records is None or len(field_records) == 0:
            raise ParameterException()
        field_list = [field_record.id for field_record in field_records]
        # 通过字段的id查询子字段的信息
        gen_field_records: List[GenFieldDO]= await genFieldMapper.select_by_db_field_ids(ids=field_list)
        if gen_field_records is None or len(gen_field_records) == 0:
            raise ParameterException()
        id_field_dict = {gen_field_record.db_field_id: gen_field_record for gen_field_record in gen_field_records}
        field_list = []
        for field_record in field_records:
            field = field_record
            gen_field= id_field_dict.get(field.id)
            field_gen = FieldGen(field=field, gen_field=gen_field)
            field_list.append(field_gen)
        table_gen: TableGen = TableGen(gen_table= gen_table, fields=field_list)
        context = Jinja2Utils.prepare_context(table_gen)
        templates = Jinja2Utils.get_template_list(gen_table.backend, gen_table.tpl_backend_type, gen_table.tpl_category,   gen_table.tpl_web_type)
        for template in templates:
            template_j2 = load_template_file(template)
            rendered_template = template_j2.render(context)
            data_map[template] = rendered_template
        return data_map


    def set_sub_table(self,*, gen_table: GenTableDO):
        pass


    def set_pk_column(self,*, gen_table: GenTableDO):
        pass