"""UserRole domain service impl"""

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
from src.main.app.mapper.sys_user_role_mapper import UserRoleMapper
from src.main.app.model.sys_user_role_model import UserRoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_user_role_schema import UserRoleQuery, UserRolePage, UserRoleDetail, UserRoleCreate, \
    UserRoleAssign
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.sys_user_role_service import UserRoleService


class UserRoleServiceImpl(ServiceBaseImpl[UserRoleMapper, UserRoleDO], UserRoleService):
    """
    Implementation of the UserRoleService interface.
    """

    def __init__(self, mapper: UserRoleMapper):
        """
        Initialize the UserRoleServiceImpl instance.

        Args:
            mapper (UserRoleMapper): The UserRoleMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_user_role_by_page(self, user_role_query: UserRoleQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if user_role_query.id is not None and user_role_query.id != "" :
            eq["id"] = user_role_query.id
        if user_role_query.role_id is not None and user_role_query.role_id != "" :
            eq["role_id"] = user_role_query.role_id
        if user_role_query.creator is not None and user_role_query.creator != "" :
            eq["creator"] = user_role_query.creator
        if user_role_query.create_time is not None and user_role_query.create_time != "" :
            eq["create_time"] = user_role_query.create_time
        if user_role_query.updater is not None and user_role_query.updater != "" :
            eq["updater"] = user_role_query.updater
        if user_role_query.deleted is not None and user_role_query.deleted != "" :
            eq["deleted"] = user_role_query.deleted
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
            current=user_role_query.current,
            pageSize=user_role_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in UserRoleDO.__fields__:
            records.sort(key=lambda x: x['sort'])
        records = [UserRolePage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_user_role_detail(self, *, id: int, request: Request) -> Optional[UserRoleDetail]:
        user_role_do: UserRoleDO =await self.mapper.select_by_id(id=id)
        if user_role_do is None:
            return None
        return UserRoleDetail(**user_role_do.model_dump())

    async def export_user_role_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        user_role_list: List[UserRoleDO] = await self.retrieve_by_ids(ids = ids)
        if user_role_list is None or len(user_role_list) == 0:
            return None
        user_role_page_list = [UserRolePage(**user_role.model_dump()) for user_role in user_role_list]
        return await export_excel(schema=UserRolePage, file_name="user_role_data_export", data_list=user_role_page_list)

    async def create_user_role(self, user_role_create: UserRoleCreate, request: Request) -> UserRoleDO:
        user_role: UserRoleDO = UserRoleDO(**user_role_create.model_dump())
        user_role.user_id = request.state.user_id
        return await self.save(data=user_role)

    async def batch_create_user_role(self, *, user_role_create_list: List[UserRoleCreate], request: Request) -> List[int]:
        user_role_list: List[UserRoleDO] = [UserRoleDO(**user_role_create.model_dump()) for user_role_create in user_role_create_list]
        await self.batch_save(datas=user_role_list)
        return [user_role.id for user_role in user_role_list]

    @staticmethod
    async def import_user_role(*, file: UploadFile, request: Request) -> Union[List[UserRoleCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_role_records = import_df.to_dict(orient="records")
        if user_role_records is None or len(user_role_records) == 0:
            return None
        for record in user_role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_role_create_list = []
        for user_role_record in user_role_records:
            try:
                user_role_create = UserRoleCreate(**user_role_record)
                user_role_create_list.append(user_role_create)
            except Exception as e:
                valid_data = {k: v for k, v in user_role_record.items() if k in UserRoleCreate.model_fields}
                user_role_create = UserRoleCreate.model_construct(**valid_data)
                user_role_create.err_msg = ValidateService.get_validate_err_msg(e)
                user_role_create_list.append(user_role_create)
                return user_role_create_list

        return user_role_create_list

    async def assign_user_role(self, user_role_assign: UserRoleAssign, request):
        user_role_records = []
        for role_id in user_role_assign.role_ids:
            user_role_records.append(UserRoleDO(user_id=user_role_assign.user_id, role_id=role_id))
        if len(user_role_records) > 0:
            await self.mapper.batch_insert(records=user_role_records)
