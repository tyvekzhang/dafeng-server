"""Role domain service impl"""

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
from src.main.app.mapper.sys_role_mapper import RoleMapper
from src.main.app.mapper.sys_role_menu_mapper import roleMenuMapper
from src.main.app.model.sys_role_menu_model import RoleMenuDO
from src.main.app.model.sys_role_model import RoleDO
from src.main.app.model.sys_user_role_model import UserRoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_schema import RoleQuery, RolePage, RoleDetail, RoleCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.sys_role_service import RoleService


class RoleServiceImpl(ServiceBaseImpl[RoleMapper, RoleDO], RoleService):
    """
    Implementation of the RoleService interface.
    """

    def __init__(self, mapper: RoleMapper):
        """
        Initialize the RoleServiceImpl instance.

        Args:
            mapper (RoleMapper): The RoleMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_role_by_page(self, role_query: RoleQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if role_query.name is not None and role_query.name != "" :
            like["name"] = role_query.name
        if role_query.code is not None and role_query.code != "" :
            eq["code"] = role_query.code
        if role_query.status is not None and role_query.status != "" :
            eq["status"] = role_query.status
        if role_query.create_time is not None and role_query.create_time != "" :
            eq["create_time"] = role_query.create_time
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
            current=role_query.current,
            pageSize=role_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in RoleDO.model_fields and len(records) > 1:
            records.sort(key=lambda x: x['sort'])
        records = [RolePage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_role_detail(self, *, id: int, request: Request) -> Optional[RoleDetail]:
        role_do: RoleDO =await self.mapper.select_by_id(id=id)
        if role_do is None:
            return None
        return RoleDetail(**role_do.model_dump())

    async def export_role_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        role_list: List[RoleDO] = await self.retrieve_by_ids(ids = ids)
        if role_list is None or len(role_list) == 0:
            return None
        role_page_list = [RolePage(**role.model_dump()) for role in role_list]
        return await export_excel(schema=RolePage, file_name="role_data_export", data_list=role_page_list)

    async def create_role(self, role_create: RoleCreate, request: Request) -> RoleDO:
        role: RoleDO = RoleDO(**role_create.model_dump())
        await self.save(data=role)
        role_menu_list = []
        for menu_id in role_create.menu_ids:
            role_menu_list.append(RoleMenuDO(role_id=role.id, menu_id=menu_id))
        await roleMenuMapper.batch_insert(records=role_menu_list)
        return role

    async def batch_create_role(self, *, role_create_list: List[RoleCreate], request: Request) -> List[int]:
        role_list: List[RoleDO] = [RoleDO(**role_create.model_dump()) for role_create in role_create_list]
        await self.batch_save(datas=role_list)
        return [role.id for role in role_list]

    @staticmethod
    async def import_role(*, file: UploadFile, request: Request) -> Union[List[RoleCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        role_records = import_df.to_dict(orient="records")
        if role_records is None or len(role_records) == 0:
            return None
        for record in role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        role_create_list = []
        for role_record in role_records:
            try:
                role_create = RoleCreate(**role_record)
                role_create_list.append(role_create)
            except Exception as e:
                valid_data = {k: v for k, v in role_record.items() if k in RoleCreate.model_fields}
                role_create = RoleCreate.model_construct(**valid_data)
                role_create.err_msg = ValidateService.get_validate_err_msg(e)
                role_create_list.append(role_create)
                return role_create_list

        return role_create_list