"""Field domain service impl"""

from sqlmodel import inspect

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.common.util.field_type_mapping_util import sqlmodel_map_to_mysql_type
from src.main.app.common.util.string_util import parse_type_params
from src.main.app.mapper.field_mapper import FieldMapper
from src.main.app.mapper.index_mapper import indexMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.field_model import FieldDO
from src.main.app.model.index_model import IndexDO
from src.main.app.model.table_model import TableDO
from src.main.app.schema.field_schema import FieldQuery
from src.main.app.service.field_service import FieldService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class FieldServiceImpl(ServiceBaseImpl[FieldMapper, FieldDO], FieldService):
    def __init__(self, mapper: FieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_fields(self, data: FieldQuery):
        table_id = data.table_id
        table_record: TableDO = await tableMapper.select_by_id(id=table_id)
        if table_record is None:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                f"{ResponseCode.PARAMETER_ERROR.msg}: {table_id}",
            )
        table_name = table_record.name
        field_name_id_map = {}
        index_name_id_map = {}
        field_records = await self.mapper.select_by_table_id(table_id=table_id)
        if field_records is not None:
            field_name_id_map = {field_record.name: field_record.id for field_record in field_records}
        engine = await get_cached_async_engine(database_id=table_record.database_id)
        async with engine.connect() as conn:
            columns = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_columns(table_name))
            indexes = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_indexes(table_name))
        indexed_columns = set()
        for index in indexes:
            for col in index["column_names"]:
                indexed_columns.add(col)
                break
        # {'comment': '年龄', 'default': None, 'name': 'age', 'nullable': True, 'type': DECIMAL(precision=10, scale=2)}
        new_add_field_records = []
        column_name_set = set()
        for column in columns:
            name = column["name"]
            column_name_set.add(name)
            if name in field_name_id_map:
                continue
            type_str = str(column["type"])
            type_name, params = parse_type_params(type_str)
            length = None
            decimals = None
            if len(params) == 1:
                length = int(list(params)[0])
            elif len(params) == 2:
                length = int(list(params)[0])
                decimals = int(list(params)[1])
            type_name = sqlmodel_map_to_mysql_type(type_name)
            nullable = column["nullable"]
            if nullable:
                not_null = 0
            else:
                not_null = 1
            new_add_field_records.append(
                FieldDO(
                    table_id=table_id,
                    name=name,
                    type=type_name,
                    length=length,
                    decimals=decimals,
                    not_null=not_null,
                    key=column["name"] in indexed_columns,
                    remark=column.get("comment", column["name"]),
                )
            )
        if len(new_add_field_records) > 0:
            await self.mapper.batch_insert(records=new_add_field_records)
        need_delete_field_ids = []
        for filed_name in field_name_id_map.keys():
            if filed_name not in column_name_set:
                need_delete_field_ids.append(field_name_id_map[filed_name])
        if len(need_delete_field_ids) > 0:
            await self.mapper.batch_delete_by_ids(ids=need_delete_field_ids)

        index_records = await indexMapper.select_by_table_id(table_id=table_id)
        if index_records is not None:
            index_name_id_map = {index_record.name: index_record.id for index_record in index_records}
        # {'column_names': ['status', 'nickname'], 'name': 'idx_status_nickname', 'unique': False}
        new_add_index_records = []
        index_name_set = set()
        for index in indexes:
            name: str = index["name"]
            index_name_set.add(name)
            if name in index_name_id_map:
                continue
            index_do = IndexDO(
                table_id=table_id,
                name=name,
                field=str(index["column_names"]).replace("[", "").replace("]", ""),
                type=str(index.get("type", "normal")).lower(),
                remark=index.get("comment", None),
            )
            new_add_index_records.append(index_do)
        if len(new_add_index_records) > 0:
            await indexMapper.batch_insert(records=new_add_index_records)
        need_delete_index_ids = []
        for index_name in index_name_id_map.keys():
            if index_name not in index_name_set:
                need_delete_index_ids.append(index_name_id_map[index_name])
        if len(need_delete_index_ids) > 0:
            await indexMapper.batch_delete_by_ids(ids=need_delete_index_ids)
        return await self.mapper.select_ordered_pagination(
            page=data.page,
            size=data.size,
            order_by=data.order_by,
            sort_order=data.sort_order,
            count=data.count,
            filter_by={"table_id": table_id},
        )
