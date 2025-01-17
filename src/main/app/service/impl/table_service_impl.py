"""Table domain service impl"""

import os.path
import subprocess
import sys
from typing import List, Any, Tuple

from sqlmodel import MetaData, inspect

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.common.session.db_engine import get_cached_async_engine
from src.main.app.common.util.field_type_mapping_util import (
    mysql_map2sqlmodel_type,
    mysql_map2server_type,
)
from src.main.app.common.util.template_util import load_template_file, resource_dir
from src.main.app.common.util.time_util import get_current_time
from src.main.app.controller.template_controller import render_template
from src.main.app.mapper.table_mapper import TableMapper
from src.main.app.model.db_table_model import TableDO
from src.main.app.schema.table_schema import TableQuery, TableAdd, TableGenerate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.table_service import TableService


class TableServiceImpl(ServiceBaseImpl[TableMapper, TableDO], TableService):
    def __init__(self, mapper: TableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_tables(self, data: TableQuery) -> Tuple[
        List[TableDO],
        int,
    ]:
        database_id = data.database_id
        engine = await get_cached_async_engine(database_id=database_id)
        async with engine.connect() as conn:
            metadata = MetaData()
            await conn.run_sync(metadata.reflect)
            table_info = []
            for table_name, table in metadata.tables.items():
                table_info.append((table_name, table.comment))
        new_add_tables = []
        need_delete_ids = []
        records: List[TableDO] = await self.mapper.select_by_database_id(database_id=database_id)
        exist_table_names = set()
        if records is not None:
            exist_table_names = {record.name: record.id for record in records}
        for table_name, table_comment in table_info:
            if table_name not in exist_table_names:
                new_add_tables.append(
                    TableDO(
                        **TableAdd(
                            database_id=database_id,
                            name=table_name,
                            comment=table_comment,
                        ).model_dump()
                    )
                )
        table_names = [table_name for table_name, table_comment in table_info]
        for table_name in exist_table_names.keys():
            if table_name not in set(table_names):
                need_delete_ids.append(exist_table_names[table_name])
        if len(new_add_tables) > 0:
            await self.mapper.batch_insert(records=new_add_tables)
        if len(need_delete_ids) > 0:
            pass
            # await self.mapper.batch_delete_by_ids(ids=need_delete_ids)
        return await self.mapper.select_by_ordered_page(
            current=data.current,
            pageSize=data.pageSize,
            order_by=data.order_by,
            sort_order=data.sort_order,
            count=data.count,
            filter_by={"database_id": database_id},
        )

    async def generate_table(self, table_generate: TableGenerate) -> None:
        database_id = table_generate.database_id
        engine = await get_cached_async_engine(database_id=database_id)

        table_name = table_generate.table_name
        async with engine.connect() as conn:
            tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            if table_name in tables:
                raise SystemException(
                    ResponseCode.TABLE_EXISTS_ERROR.code,
                    f"{ResponseCode.TABLE_EXISTS_ERROR.msg}: {table_name}",
                )
        template = load_template_file(template_name="default/table_create.py.j2")
        if table_generate.class_name is None:
            table_name_split = table_generate.table_name.split("_")
            if len(table_name_split) == 1:
                table_generate.class_name = table_name_split[0].title()
            else:
                table_generate.class_name = table_name_split[1].title()
        table_generate.field_metadata = list(
            map(
                lambda item: item.model_copy(
                    update={
                        "modeltype": mysql_map2sqlmodel_type(item.type),
                        "server_type": mysql_map2server_type(item.type),
                    }
                ),
                table_generate.field_metadata,
            )
        )
        rendered_content = render_template(template, **table_generate.model_dump())
        dest_dir = os.path.join(resource_dir, "table_create_history")
        file_name = f"{get_current_time("%Y-%m-%d-%H-%M")}_{table_generate.table_name}.py"
        dest_path = os.path.join(dest_dir, file_name)
        with open(dest_path, "w", encoding="UTF-8") as f:
            f.write(rendered_content)
        try:
            subprocess.run([sys.executable, dest_path], capture_output=True, text=True, check=True)
        except:
            pass
