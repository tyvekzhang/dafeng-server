"""GlobalWord domain service impl"""

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
from src.main.app.mapper.read_global_word_mapper import GlobalWordMapper
from src.main.app.model.read_global_word_model import GlobalWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_global_word_schema import GlobalWordQuery, GlobalWordPage, GlobalWordDetail, GlobalWordCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.read_global_word_service import GlobalWordService


class GlobalWordServiceImpl(ServiceBaseImpl[GlobalWordMapper, GlobalWordDO], GlobalWordService):
    """
    Implementation of the GlobalWordService interface.
    """

    def __init__(self, mapper: GlobalWordMapper):
        """
        Initialize the GlobalWordServiceImpl instance.

        Args:
            mapper (GlobalWordMapper): The GlobalWordMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_global_word_by_page(self, global_word_query: GlobalWordQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if global_word_query.id is not None and global_word_query.id != "" :
            eq["id"] = global_word_query.id
        if global_word_query.word is not None and global_word_query.word != "" :
            eq["word"] = global_word_query.word
        if global_word_query.pronunciation is not None and global_word_query.pronunciation != "" :
            eq["pronunciation"] = global_word_query.pronunciation
        if global_word_query.pronunciationUs is not None and global_word_query.pronunciationUs != "" :
            eq["pronunciationUs"] = global_word_query.pronunciationUs
        if global_word_query.definition is not None and global_word_query.definition != "" :
            eq["definition"] = global_word_query.definition
        if global_word_query.example is not None and global_word_query.example != "" :
            eq["example"] = global_word_query.example
        if global_word_query.translation is not None and global_word_query.translation != "" :
            eq["translation"] = global_word_query.translation
        if global_word_query.wordSrc is not None and global_word_query.wordSrc != "" :
            eq["wordSrc"] = global_word_query.wordSrc
        if global_word_query.wordSrcUs is not None and global_word_query.wordSrcUs != "" :
            eq["wordSrcUs"] = global_word_query.wordSrcUs
        if global_word_query.exampleSrc is not None and global_word_query.exampleSrc != "" :
            eq["exampleSrc"] = global_word_query.exampleSrc
        if global_word_query.pluralForm is not None and global_word_query.pluralForm != "" :
            eq["pluralForm"] = global_word_query.pluralForm
        if global_word_query.thirdPersonSingular is not None and global_word_query.thirdPersonSingular != "" :
            eq["thirdPersonSingular"] = global_word_query.thirdPersonSingular
        if global_word_query.presentTenseContinuous is not None and global_word_query.presentTenseContinuous != "" :
            eq["presentTenseContinuous"] = global_word_query.presentTenseContinuous
        if global_word_query.pastTense is not None and global_word_query.pastTense != "" :
            eq["pastTense"] = global_word_query.pastTense
        if global_word_query.pastParticiple is not None and global_word_query.pastParticiple != "" :
            eq["pastParticiple"] = global_word_query.pastParticiple
        if global_word_query.level is not None and global_word_query.level != "" :
            eq["level"] = global_word_query.level
        if global_word_query.version is not None and global_word_query.version != "" :
            eq["version"] = global_word_query.version
        if global_word_query.tag is not None and global_word_query.tag != "" :
            eq["tag"] = global_word_query.tag
        if global_word_query.status is not None and global_word_query.status != "" :
            eq["status"] = global_word_query.status
        if global_word_query.createTime is not None and global_word_query.createTime != "" :
            eq["createTime"] = global_word_query.createTime
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
            current=global_word_query.current,
            pageSize=global_word_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in GlobalWordDO.__fields__:
            records.sort(key=lambda x: x['sort'])
        records = [GlobalWordPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_global_word_detail(self, *, id: int, request: Request) -> Optional[GlobalWordDetail]:
        global_word_do: GlobalWordDO =await self.mapper.select_by_id(id=id)
        if global_word_do is None:
            return None
        return GlobalWordDetail(**global_word_do.model_dump())

    async def export_global_word_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        global_word_list: List[GlobalWordDO] = await self.retrieve_by_ids(ids = ids)
        if global_word_list is None or len(global_word_list) == 0:
            return None
        global_word_page_list = [GlobalWordPage(**global_word.model_dump()) for global_word in global_word_list]
        return await export_excel(schema=GlobalWordPage, file_name="global_word_data_export", data_list=global_word_page_list)

    async def create_global_word(self, global_word_create: GlobalWordCreate, request: Request) -> GlobalWordDO:
        global_word: GlobalWordDO = GlobalWordDO(**global_word_create.model_dump())
        # global_word.user_id = request.state.user_id
        return await self.save(data=global_word)

    async def batch_create_global_word(self, *, global_word_create_list: List[GlobalWordCreate], request: Request) -> List[int]:
        global_word_list: List[GlobalWordDO] = [GlobalWordDO(**global_word_create.model_dump()) for global_word_create in global_word_create_list]
        await self.batch_save(datas=global_word_list)
        return [global_word.id for global_word in global_word_list]

    @staticmethod
    async def import_global_word(*, file: UploadFile, request: Request) -> Union[List[GlobalWordCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        global_word_records = import_df.to_dict(orient="records")
        if global_word_records is None or len(global_word_records) == 0:
            return None
        for record in global_word_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        global_word_create_list = []
        for global_word_record in global_word_records:
            try:
                global_word_create = GlobalWordCreate(**global_word_record)
                global_word_create_list.append(global_word_create)
            except Exception as e:
                valid_data = {k: v for k, v in global_word_record.items() if k in GlobalWordCreate.model_fields}
                global_word_create = GlobalWordCreate.model_construct(**valid_data)
                global_word_create.err_msg = ValidateService.get_validate_err_msg(e)
                global_word_create_list.append(global_word_create)
                return global_word_create_list

        return global_word_create_list