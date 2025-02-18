"""GlobalWord 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.read_global_word_mapper import globalWordMapper
from src.main.app.model.read_global_word_model import GlobalWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_global_word_schema import GlobalWordQuery, GlobalWordModify, GlobalWordCreate, \
    GlobalWordBatchModify, GlobalWordDetail
from src.main.app.service.impl.read_global_word_service_impl import GlobalWordServiceImpl
from src.main.app.service.read_global_word_service import GlobalWordService

global_word_router = APIRouter()
global_word_service: GlobalWordService = GlobalWordServiceImpl(mapper=globalWordMapper)

@global_word_router.get("/page")
async def fetch_global_word_by_page(
    global_word_query: Annotated[GlobalWordQuery, Query()], request: Request
) -> Dict[str, Any]:
    global_word_page_result: PageResult = await global_word_service.fetch_global_word_by_page(
        global_word_query=global_word_query,
        request=request
    )
    return HttpResponse.success(global_word_page_result)

@global_word_router.get("/detail/{id}")
async def fetch_global_word_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    global_word_detail: GlobalWordDetail = await global_word_service.fetch_global_word_detail(id=id, request=request)
    return HttpResponse.success(global_word_detail)

@global_word_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=GlobalWordCreate, file_name="global_word_import_tpl")

@global_word_router.get("/export")
async def export_global_word_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await global_word_service.export_global_word_page(ids=ids, request=request)

@global_word_router.post("/create")
async def create_global_word(
    global_word_create: GlobalWordCreate, request: Request
) -> Dict[str, Any]:
    global_word: GlobalWordDO = await global_word_service.create_global_word(global_word_create=global_word_create, request=request)
    return HttpResponse.success(global_word.id)

@global_word_router.post("/batch-create")
async def batch_create_global_word(
    global_word_create_list: List[GlobalWordCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await global_word_service.batch_create_global_word(global_word_create_list=global_word_create_list, request=request)
    return HttpResponse.success(ids)

@global_word_router.post("/import")
async def import_global_word(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    global_word_create_list: List[GlobalWordCreate] = await global_word_service.import_global_word(file=file, request=request)
    return HttpResponse.success(global_word_create_list)

@global_word_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await global_word_service.remove_by_id(id=id)
    return HttpResponse.success()

@global_word_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await global_word_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@global_word_router.put("/modify")
async def modify(
    global_word_modify: GlobalWordModify, request: Request
) -> Dict[str, Any]:
    await global_word_service.modify_by_id(data=GlobalWordDO(**global_word_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@global_word_router.put("/batch-modify")
async def batch_modify(global_word_batch_modify: GlobalWordBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in global_word_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await global_word_service.batch_modify_by_ids(ids=global_word_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()