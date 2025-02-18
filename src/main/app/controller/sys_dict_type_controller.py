"""DictType 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_dict_type_mapper import dictTypeMapper
from src.main.app.model.sys_dict_type_model import DictTypeDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_dict_type_schema import DictTypeQuery, DictTypeModify, DictTypeCreate, \
    DictTypeBatchModify, DictTypeDetail
from src.main.app.service.impl.sys_dict_type_service_impl import DictTypeServiceImpl
from src.main.app.service.sys_dict_type_service import DictTypeService

dict_type_router = APIRouter()
dict_type_service: DictTypeService = DictTypeServiceImpl(mapper=dictTypeMapper)

@dict_type_router.get("/page")
async def fetch_dict_type_by_page(
    dict_type_query: Annotated[DictTypeQuery, Query()], request: Request
) -> Dict[str, Any]:
    dict_type_page_result: PageResult = await dict_type_service.fetch_dict_type_by_page(
        dict_type_query=dict_type_query,
        request=request
    )
    return HttpResponse.success(dict_type_page_result)

@dict_type_router.get("/detail/{id}")
async def fetch_dict_type_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    dict_type_detail: DictTypeDetail = await dict_type_service.fetch_dict_type_detail(id=id, request=request)
    return HttpResponse.success(dict_type_detail)

@dict_type_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=DictTypeCreate, file_name="dict_type_import_tpl")

@dict_type_router.get("/export")
async def export_dict_type_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await dict_type_service.export_dict_type_page(ids=ids, request=request)

@dict_type_router.post("/create")
async def create_dict_type(
    dict_type_create: DictTypeCreate, request: Request
) -> Dict[str, Any]:
    dict_type: DictTypeDO = await dict_type_service.create_dict_type(dict_type_create=dict_type_create, request=request)
    return HttpResponse.success(dict_type.id)

@dict_type_router.post("/batch-create")
async def batch_create_dict_type(
    dict_type_create_list: List[DictTypeCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await dict_type_service.batch_create_dict_type(dict_type_create_list=dict_type_create_list, request=request)
    return HttpResponse.success(ids)

@dict_type_router.post("/import")
async def import_dict_type(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    dict_type_create_list: List[DictTypeCreate] = await dict_type_service.import_dict_type(file=file, request=request)
    return HttpResponse.success(dict_type_create_list)

@dict_type_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await dict_type_service.remove_by_id(id=id)
    return HttpResponse.success()

@dict_type_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await dict_type_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@dict_type_router.put("/modify")
async def modify(
    dict_type_modify: DictTypeModify, request: Request
) -> Dict[str, Any]:
    await dict_type_service.modify_by_id(data=DictTypeDO(**dict_type_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@dict_type_router.put("/batch-modify")
async def batch_modify(dict_type_batch_modify: DictTypeBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in dict_type_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await dict_type_service.batch_modify_by_ids(ids=dict_type_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()