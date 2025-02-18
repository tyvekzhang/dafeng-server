"""NewWord domain service impl"""

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
from src.main.app.mapper.read_new_word_mapper import NewWordMapper
from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_new_word_schema import NewWordQuery, NewWordPage, NewWordDetail, NewWordCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.read_new_word_service import NewWordService


class NewWordServiceImpl(ServiceBaseImpl[NewWordMapper, NewWordDO], NewWordService):
    """
    Implementation of the NewWordService interface.
    """

    def __init__(self, mapper: NewWordMapper):
        """
        Initialize the NewWordServiceImpl instance.

        Args:
            mapper (NewWordMapper): The NewWordMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_new_word_by_page(self, new_word_query: NewWordQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if new_word_query.id is not None and new_word_query.id != "" :
            eq["id"] = new_word_query.id
        if new_word_query.word is not None and new_word_query.word != "" :
            eq["word"] = new_word_query.word
        if new_word_query.translation is not None and new_word_query.translation != "" :
            eq["translation"] = new_word_query.translation
        if new_word_query.next_review_date is not None and new_word_query.next_review_date != "" :
            eq["next_review_date"] = new_word_query.next_review_date
        if new_word_query.tenant is not None and new_word_query.tenant != "" :
            eq["tenant"] = new_word_query.tenant
        if new_word_query.update_time is not None and new_word_query.update_time != "" :
            eq["update_time"] = new_word_query.update_time
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
            current=new_word_query.current,
            pageSize=new_word_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in NewWordDO.__fields__:
            records.sort(key=lambda x: x['sort'])
        records = [NewWordPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_new_word_detail(self, *, id: int, request: Request) -> Optional[NewWordDetail]:
        new_word_do: NewWordDO =await self.mapper.select_by_id(id=id)
        if new_word_do is None:
            return None
        return NewWordDetail(**new_word_do.model_dump())

    async def export_new_word_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        new_word_list: List[NewWordDO] = await self.retrieve_by_ids(ids = ids)
        if new_word_list is None or len(new_word_list) == 0:
            return None
        new_word_page_list = [NewWordPage(**new_word.model_dump()) for new_word in new_word_list]
        return await export_excel(schema=NewWordPage, file_name="new_word_data_export", data_list=new_word_page_list)

    async def create_new_word(self, new_word_create: NewWordCreate, request: Request) -> NewWordDO:
        new_word: NewWordDO = NewWordDO(**new_word_create.model_dump())
        # new_word.user_id = request.state.user_id
        return await self.save(data=new_word)

    async def batch_create_new_word(self, *, new_word_create_list: List[NewWordCreate], request: Request) -> List[int]:
        new_word_list: List[NewWordDO] = [NewWordDO(**new_word_create.model_dump()) for new_word_create in new_word_create_list]
        await self.batch_save(datas=new_word_list)
        return [new_word.id for new_word in new_word_list]

    @staticmethod
    async def import_new_word(*, file: UploadFile, request: Request) -> Union[List[NewWordCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        new_word_records = import_df.to_dict(orient="records")
        if new_word_records is None or len(new_word_records) == 0:
            return None
        for record in new_word_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        new_word_create_list = []
        for new_word_record in new_word_records:
            try:
                new_word_create = NewWordCreate(**new_word_record)
                new_word_create_list.append(new_word_create)
            except Exception as e:
                valid_data = {k: v for k, v in new_word_record.items() if k in NewWordCreate.model_fields}
                new_word_create = NewWordCreate.model_construct(**valid_data)
                new_word_create.err_msg = ValidateService.get_validate_err_msg(e)
                new_word_create_list.append(new_word_create)
                return new_word_create_list

        return new_word_create_list