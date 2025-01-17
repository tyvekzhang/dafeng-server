"""NewWord domain service impl"""
from __future__ import annotations

from typing import Optional, List, Union

from pydantic_core._pydantic_core import ValidationError
from starlette.responses import StreamingResponse
from fastapi import UploadFile
import io
from collections import Counter
from datetime import timedelta, datetime
from starlette.responses import StreamingResponse
from fastapi import UploadFile
from typing import Optional, List
import pandas as pd

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.enums.enum import ResponseCode, TokenTypeEnum
from src.main.app.common.exception.exception import ServiceException, SystemException
from src.main.app.common.util.validate_util import ValidateService
from src.main.app.mapper.user_mapper import UserMapper
from src.main.app.schema.common_schema import Token
from src.main.app.schema.user_schema import (
    UserAdd,
    LoginCmd,
    UserQuery,
    UserFilterForm,
)
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.user_service import UserService
from src.main.app.model.user_model import UserDO
from src.main.app.common.util import security_util
from src.main.app.common.util.excel_util import export_excel
from src.main.app.common.util.security_util import get_password_hash, verify_password


from src.main.app.common.util.excel_util import export_excel
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

    async def fetch_new_word_by_page(self, new_word_query: NewWordQuery) -> PageResult:
        records, total = await self.mapper.select_by_ordered_page(
            current=new_word_query.current,
            pageSize=new_word_query.pageSize,
        )
        records = [NewWordPage(id=record.id, word=record.word) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_new_word_detail(self, *, id: int) -> Optional[NewWordDetail]:
        new_word_do: NewWordDO =await self.mapper.select_by_id(id=id)
        if new_word_do is None:
            return None
        return NewWordDetail(**new_word_do.model_dump())

    async def export_new_word_page(self, *, ids: List[int]) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        new_word_list: List[NewWordDO] = await self.retrieve_by_ids(ids = ids)
        if new_word_list is None or len(new_word_list) == 0:
            return None
        new_word_page_list = [NewWordPage(**new_word.model_dump()) for new_word in new_word_list]
        return await export_excel(schema=NewWordPage, file_name="阅读生词数据导出", data_list=new_word_page_list)

    async def create_new_word(self, new_word_create: NewWordCreate) -> NewWordDO:
        new_word: NewWordDO = NewWordDO(**new_word_create.model_dump())
        return await self.save(data=new_word)

    async def batch_create_new_word(self, *, new_word_create_list: List[NewWordCreate]) -> List[int]:
        new_word_list: List[NewWordDO] = [NewWordDO(**new_word_create.model_dump()) for new_word_create in new_word_create_list]
        await self.save(new_word_list)
        return [new_word.id for new_word in new_word_list]

    @staticmethod
    async def import_new_word(*, file: UploadFile) -> Union[List[NewWordCreate], None]:
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
            except ValidationError as e:
                valid_data = {k: v for k, v in new_word_record.items() if k in NewWordCreate.model_fields}
                new_word_create = NewWordCreate.model_construct(**valid_data)
                new_word_create.err_msg = ValidateService.get_validate_err_msg(e)
                new_word_create_list.append(new_word_create)
        return new_word_create_list