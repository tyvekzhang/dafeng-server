"""Member domain service impl"""

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
from src.main.app.mapper.member_mapper import MemberMapper
from src.main.app.model.member_model import MemberDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.member_schema import MemberQuery, MemberPage, MemberDetail, MemberCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.member_service import MemberService


class MemberServiceImpl(ServiceBaseImpl[MemberMapper, MemberDO], MemberService):
    """
    Implementation of the MemberService interface.
    """

    def __init__(self, mapper: MemberMapper):
        """
        Initialize the MemberServiceImpl instance.

        Args:
            mapper (MemberMapper): The MemberMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_member_by_page(self, member_query: MemberQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if member_query.id is not None and member_query.id != "" :
            eq["id"] = member_query.id
        if member_query.name is not None and member_query.name != "" :
            like["name"] = member_query.name
        if member_query.nation is not None and member_query.nation != "" :
            eq["nation"] = member_query.nation
        if member_query.gender is not None and member_query.gender != "" :
            eq["gender"] = member_query.gender
        if member_query.birthday is not None and member_query.birthday != "" :
            eq["birthday"] = member_query.birthday
        if member_query.hobby is not None and member_query.hobby != "" :
            eq["hobby"] = member_query.hobby
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
            current=member_query.current,
            pageSize=member_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in MemberDO.__fields__:
            records.sort(key=lambda x: x['sort'])
        records = [MemberPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_member_detail(self, *, id: int, request: Request) -> Optional[MemberDetail]:
        member_do: MemberDO =await self.mapper.select_by_id(id=id)
        if member_do is None:
            return None
        return MemberDetail(**member_do.model_dump())

    async def export_member_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        member_list: List[MemberDO] = await self.retrieve_by_ids(ids = ids)
        if member_list is None or len(member_list) == 0:
            return None
        member_page_list = [MemberPage(**member.model_dump()) for member in member_list]
        return await export_excel(schema=MemberPage, file_name="member_data_export", data_list=member_page_list)

    async def create_member(self, member_create: MemberCreate, request: Request) -> MemberDO:
        member: MemberDO = MemberDO(**member_create.model_dump())
        # member.user_id = request.state.user_id
        return await self.save(data=member)

    async def batch_create_member(self, *, member_create_list: List[MemberCreate], request: Request) -> List[int]:
        member_list: List[MemberDO] = [MemberDO(**member_create.model_dump()) for member_create in member_create_list]
        await self.batch_save(datas=member_list)
        return [member.id for member in member_list]

    @staticmethod
    async def import_member(*, file: UploadFile, request: Request) -> Union[List[MemberCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        member_records = import_df.to_dict(orient="records")
        if member_records is None or len(member_records) == 0:
            return None
        for record in member_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        member_create_list = []
        for member_record in member_records:
            try:
                member_create = MemberCreate(**member_record)
                member_create_list.append(member_create)
            except Exception as e:
                valid_data = {k: v for k, v in member_record.items() if k in MemberCreate.model_fields}
                member_create = MemberCreate.model_construct(**valid_data)
                member_create.err_msg = ValidateService.get_validate_err_msg(e)
                member_create_list.append(member_create)
                return member_create_list

        return member_create_list