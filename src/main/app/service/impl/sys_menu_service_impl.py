"""Menu domain service impl"""

from __future__ import annotations
import io
from typing import Optional, List
from typing import Union
import pandas as pd
from fastapi import UploadFile, Request
from fastapi.exceptions import ResponseValidationError
from starlette.responses import StreamingResponse
from src.main.app.common.enums.enum import FilterOperators
from src.main.app.common.util.excel_util import export_excel
from src.main.app.common.util.tree_util import list_to_tree
from src.main.app.common.util.validate_util import ValidateService
from src.main.app.mapper.sys_menu_mapper import MenuMapper
from src.main.app.model.sys_menu_model import MenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_menu_schema import MenuQuery, MenuPage, MenuDetail, MenuCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.sys_menu_service import MenuService


class MenuServiceImpl(ServiceBaseImpl[MenuMapper, MenuDO], MenuService):
    """
    Implementation of the MenuService interface.
    """

    def __init__(self, mapper: MenuMapper):
        """
        Initialize the MenuServiceImpl instance.

        Args:
            mapper (MenuMapper): The MenuMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_menu_by_page(self, menu_query: MenuQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if menu_query.name is not None and menu_query.name != "" :
            like["name"] = menu_query.name
        if menu_query.status is not None and menu_query.status != "" :
            eq["status"] = menu_query.status
        if menu_query.create_time is not None and menu_query.create_time != "" :
            eq["create_time"] = menu_query.create_time
        filters = {
            FilterOperators.EQ: eq,
            FilterOperators.NE: ne,
            FilterOperators.GT: gt,
            FilterOperators.GE: ge,
            FilterOperators.LT: lt,
            FilterOperators.LE: le,
            FilterOperators.BETWEEN: between,
            FilterOperators.LIKE: like
        }
        records, total = await self.mapper.select_by_ordered_page(
            current=menu_query.current,
            pageSize=menu_query.pageSize,
            **filters
        )
        records = [MenuPage(**record.model_dump()) for record in records]
        records = [record.model_dump() for record in records]
        records = list_to_tree(records)
        return PageResult(records=records, total=total)

    async def fetch_menu_detail(self, *, id: int, request: Request) -> Optional[MenuDetail]:
        menu_do: MenuDO =await self.mapper.select_by_id(id=id)
        if menu_do is None:
            return None
        return MenuDetail(**menu_do.model_dump())

    async def export_menu_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        menu_list: List[MenuDO] = await self.retrieve_by_ids(ids = ids)
        if menu_list is None or len(menu_list) == 0:
            return None
        menu_page_list = [MenuPage(**menu.model_dump()) for menu in menu_list]
        return await export_excel(schema=MenuPage, file_name="menu_data_export", data_list=menu_page_list)

    async def create_menu(self, menu_create: MenuCreate, request: Request) -> MenuDO:
        menu: MenuDO = MenuDO(**menu_create.model_dump())
        menu.user_id = request.state.user_id
        return await self.save(data=menu)

    async def batch_create_menu(self, *, menu_create_list: List[MenuCreate], request: Request) -> List[int]:
        menu_list: List[MenuDO] = [MenuDO(**menu_create.model_dump()) for menu_create in menu_create_list]
        await self.batch_save(datas=menu_list)
        return [menu.id for menu in menu_list]

    @staticmethod
    async def import_menu(*, file: UploadFile, request: Request) -> Union[List[MenuCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        menu_records = import_df.to_dict(orient="records")
        if menu_records is None or len(menu_records) == 0:
            return None
        for record in menu_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        menu_create_list = []
        for menu_record in menu_records:
            try:
                menu_create = MenuCreate(**menu_record)
                menu_create_list.append(menu_create)
            except Exception as e:
                valid_data = {k: v for k, v in menu_record.items() if k in MenuCreate.model_fields}
                menu_create = MenuCreate.model_construct(**valid_data)
                menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                menu_create_list.append(menu_create)
                return menu_create_list

        return menu_create_list