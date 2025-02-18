"""DictData 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_dict_data_mapper import dictDataMapper
from src.main.app.model.sys_dict_data_model import DictDataDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_dict_data_schema import DictDataQuery, DictDataModify, DictDataCreate, \
    DictDataBatchModify, DictDataDetail
from src.main.app.service.impl.sys_dict_data_service_impl import DictDataServiceImpl
from src.main.app.service.sys_dict_data_service import DictDataService

dict_data_router = APIRouter()
dict_data_service: DictDataService = DictDataServiceImpl(mapper=dictDataMapper)

@dict_data_router.get("/page")
async def fetch_dict_data_by_page(
    dict_data_query: Annotated[DictDataQuery, Query()], request: Request
) -> Dict[str, Any]:
    dict_data_page_result: PageResult = await dict_data_service.fetch_dict_data_by_page(
        dict_data_query=dict_data_query,
        request=request
    )
    return HttpResponse.success(dict_data_page_result)

@dict_data_router.get("/all")
async def get_all_data(request: Request) -> Dict[str, Any]:
    return HttpResponse.success(await dict_data_service.get_all_data(request))

@dict_data_router.get("/detail/{id}")
async def fetch_dict_data_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    dict_data_detail: DictDataDetail = await dict_data_service.fetch_dict_data_detail(id=id, request=request)
    return HttpResponse.success(dict_data_detail)

@dict_data_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=DictDataCreate, file_name="dict_data_import_tpl")

@dict_data_router.get("/export")
async def export_dict_data_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await dict_data_service.export_dict_data_page(ids=ids, request=request)

@dict_data_router.post("/create")
async def create_dict_data(
    dict_data_create: DictDataCreate, request: Request
) -> Dict[str, Any]:
    dict_data: DictDataDO = await dict_data_service.create_dict_data(dict_data_create=dict_data_create, request=request)
    return HttpResponse.success(dict_data.id)

@dict_data_router.post("/batch-create")
async def batch_create_dict_data(
    dict_data_create_list: List[DictDataCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await dict_data_service.batch_create_dict_data(dict_data_create_list=dict_data_create_list, request=request)
    return HttpResponse.success(ids)

@dict_data_router.post("/import")
async def import_dict_data(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    dict_data_create_list: List[DictDataCreate] = await dict_data_service.import_dict_data(file=file, request=request)
    return HttpResponse.success(dict_data_create_list)

@dict_data_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await dict_data_service.remove_by_id(id=id)
    return HttpResponse.success()

@dict_data_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await dict_data_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@dict_data_router.put("/modify")
async def modify(
    dict_data_modify: DictDataModify, request: Request
) -> Dict[str, Any]:
    await dict_data_service.modify_by_id(data=DictDataDO(**dict_data_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@dict_data_router.put("/batch-modify")
async def batch_modify(dict_data_batch_modify: DictDataBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in dict_data_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await dict_data_service.batch_modify_by_ids(ids=dict_data_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()