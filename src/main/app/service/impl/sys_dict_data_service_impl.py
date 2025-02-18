"""DictData domain service impl"""

from __future__ import annotations
import io
from typing import Optional, List, Dict
from typing import Union
import pandas as pd
from fastapi import UploadFile, Request
from fastapi.exceptions import ResponseValidationError
from starlette.responses import StreamingResponse
from src.main.app.common.enums.enum import FilterOperators
from src.main.app.common.util.excel_util import export_excel
from src.main.app.common.util.validate_util import ValidateService
from src.main.app.mapper.sys_dict_data_mapper import DictDataMapper
from src.main.app.model.sys_dict_data_model import DictDataDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_dict_data_schema import DictDataQuery, DictDataPage, DictDataDetail, DictDataCreate
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.service.sys_dict_data_service import DictDataService


class DictDataServiceImpl(ServiceBaseImpl[DictDataMapper, DictDataDO], DictDataService):
    """
    Implementation of the DictDataService interface.
    """

    def __init__(self, mapper: DictDataMapper):
        """
        Initialize the DictDataServiceImpl instance.

        Args:
            mapper (DictDataMapper): The DictDataMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_dict_data_by_page(self, dict_data_query: DictDataQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if dict_data_query.id is not None and dict_data_query.id != "" :
            eq["id"] = dict_data_query.id
        if dict_data_query.sort is not None and dict_data_query.sort != "" :
            eq["sort"] = dict_data_query.sort
        if dict_data_query.label is not None and dict_data_query.label != "" :
            eq["label"] = dict_data_query.label
        if dict_data_query.value is not None and dict_data_query.value != "" :
            eq["value"] = dict_data_query.value
        if dict_data_query.type is not None and dict_data_query.value != "" :
            eq["type"] = dict_data_query.type
        if dict_data_query.is_default is not None and dict_data_query.is_default != "" :
            eq["is_default"] = dict_data_query.is_default
        if dict_data_query.status is not None and dict_data_query.status != "" :
            eq["status"] = dict_data_query.status
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
            current=dict_data_query.current,
            pageSize=dict_data_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in DictDataDO.model_fields and total > 1:
            records = sorted(records, key=lambda x: x.sort)
        records = [DictDataPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_dict_data_detail(self, *, id: int, request: Request) -> Optional[DictDataDetail]:
        dict_data_do: DictDataDO =await self.mapper.select_by_id(id=id)
        if dict_data_do is None:
            return None
        return DictDataDetail(**dict_data_do.model_dump())

    async def export_dict_data_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        dict_data_list: List[DictDataDO] = await self.retrieve_by_ids(ids = ids)
        if dict_data_list is None or len(dict_data_list) == 0:
            return None
        dict_data_page_list = [DictDataPage(**dict_data.model_dump()) for dict_data in dict_data_list]
        return await export_excel(schema=DictDataPage, file_name="dict_data_data_export", data_list=dict_data_page_list)

    async def create_dict_data(self, dict_data_create: DictDataCreate, request: Request) -> DictDataDO:
        dict_data: DictDataDO = DictDataDO(**dict_data_create.model_dump())
        # dict_data.user_id = request.state.user_id
        return await self.save(data=dict_data)

    async def batch_create_dict_data(self, *, dict_data_create_list: List[DictDataCreate], request: Request) -> List[int]:
        dict_data_list: List[DictDataDO] = [DictDataDO(**dict_data_create.model_dump()) for dict_data_create in dict_data_create_list]
        await self.batch_save(datas=dict_data_list)
        return [dict_data.id for dict_data in dict_data_list]

    @staticmethod
    async def import_dict_data(*, file: UploadFile, request: Request) -> Union[List[DictDataCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        dict_data_records = import_df.to_dict(orient="records")
        if dict_data_records is None or len(dict_data_records) == 0:
            return None
        for record in dict_data_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        dict_data_create_list = []
        for dict_data_record in dict_data_records:
            try:
                dict_data_create = DictDataCreate(**dict_data_record)
                dict_data_create_list.append(dict_data_create)
            except Exception as e:
                valid_data = {k: v for k, v in dict_data_record.items() if k in DictDataCreate.model_fields}
                dict_data_create = DictDataCreate.model_construct(**valid_data)
                dict_data_create.err_msg = ValidateService.get_validate_err_msg(e)
                dict_data_create_list.append(dict_data_create)
                return dict_data_create_list

        return dict_data_create_list

    async def get_all_data(self, request: Request) -> Dict[str, any]:
       all_data, total_count =  await self.mapper.select_by_ordered_page(current=1, pageSize=9999)
       if total_count == 0:
           return {}
       result = {}
       for item in all_data:
           item = item.model_dump()
           item_type = item["type"]
           label_value = {"value": item["value"], "label": item["label"]}
           if item_type not in result:
               result[item_type] = []
           result[item_type].append(label_value)
       return result