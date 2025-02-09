"""RoleMenu domain service impl"""

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
from src.main.app.common.util.validate_util import ValidateService
from src.main.app.mapper.sys_role_menu_mapper import RoleMenuMapper
from src.main.app.model.sys_role_menu_model import RoleMenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_menu_schema import RoleMenuQuery, RoleMenuPage, RoleMenuDetail, RoleMenuCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.sys_role_menu_service import RoleMenuService


class RoleMenuServiceImpl(ServiceBaseImpl[RoleMenuMapper, RoleMenuDO], RoleMenuService):
    """
    Implementation of the RoleMenuService interface.
    """

    def __init__(self, mapper: RoleMenuMapper):
        """
        Initialize the RoleMenuServiceImpl instance.

        Args:
            mapper (RoleMenuMapper): The RoleMenuMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_role_menu_by_page(self, role_menu_query: RoleMenuQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if role_menu_query.id is not None and role_menu_query.id != "" :
            eq["id"] = role_menu_query.id
        if role_menu_query.role_id is not None and role_menu_query.role_id != "" :
            eq["role_id"] = role_menu_query.role_id
        if role_menu_query.menu_id is not None and role_menu_query.menu_id != "" :
            eq["menu_id"] = role_menu_query.menu_id
        if role_menu_query.creator is not None and role_menu_query.creator != "" :
            eq["creator"] = role_menu_query.creator
        if role_menu_query.create_time is not None and role_menu_query.create_time != "" :
            eq["create_time"] = role_menu_query.create_time
        if role_menu_query.updater is not None and role_menu_query.updater != "" :
            eq["updater"] = role_menu_query.updater
        if role_menu_query.deleted is not None and role_menu_query.deleted != "" :
            eq["deleted"] = role_menu_query.deleted
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
            current=role_menu_query.current,
            pageSize=role_menu_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in RoleMenuDO.__fields__:
            records.sort(key=lambda x: x['sort'])
        records = [RoleMenuPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_role_menu_detail(self, *, id: int, request: Request) -> Optional[RoleMenuDetail]:
        role_menu_do: RoleMenuDO =await self.mapper.select_by_id(id=id)
        if role_menu_do is None:
            return None
        return RoleMenuDetail(**role_menu_do.model_dump())

    async def export_role_menu_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        role_menu_list: List[RoleMenuDO] = await self.retrieve_by_ids(ids = ids)
        if role_menu_list is None or len(role_menu_list) == 0:
            return None
        role_menu_page_list = [RoleMenuPage(**role_menu.model_dump()) for role_menu in role_menu_list]
        return await export_excel(schema=RoleMenuPage, file_name="role_menu_data_export", data_list=role_menu_page_list)

    async def create_role_menu(self, role_menu_create: RoleMenuCreate, request: Request) -> RoleMenuDO:
        role_menu: RoleMenuDO = RoleMenuDO(**role_menu_create.model_dump())
        role_menu.user_id = request.state.user_id
        return await self.save(data=role_menu)

    async def batch_create_role_menu(self, *, role_menu_create_list: List[RoleMenuCreate], request: Request) -> List[int]:
        role_menu_list: List[RoleMenuDO] = [RoleMenuDO(**role_menu_create.model_dump()) for role_menu_create in role_menu_create_list]
        await self.batch_save(datas=role_menu_list)
        return [role_menu.id for role_menu in role_menu_list]

    @staticmethod
    async def import_role_menu(*, file: UploadFile, request: Request) -> Union[List[RoleMenuCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        role_menu_records = import_df.to_dict(orient="records")
        if role_menu_records is None or len(role_menu_records) == 0:
            return None
        for record in role_menu_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        role_menu_create_list = []
        for role_menu_record in role_menu_records:
            try:
                role_menu_create = RoleMenuCreate(**role_menu_record)
                role_menu_create_list.append(role_menu_create)
            except Exception as e:
                valid_data = {k: v for k, v in role_menu_record.items() if k in RoleMenuCreate.model_fields}
                role_menu_create = RoleMenuCreate.model_construct(**valid_data)
                role_menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                role_menu_create_list.append(role_menu_create)
                return role_menu_create_list

        return role_menu_create_list