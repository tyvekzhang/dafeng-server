"""NewWord 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.read_new_word_mapper import newWordMapper
from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_new_word_schema import NewWordQuery, NewWordModify, NewWordCreate, \
    NewWordBatchModify, NewWordDetail
from src.main.app.service.impl.read_new_word_service_impl import NewWordServiceImpl
from src.main.app.service.read_new_word_service import NewWordService

new_word_router = APIRouter()
new_word_service: NewWordService = NewWordServiceImpl(mapper=newWordMapper)

@new_word_router.get("/page")
async def fetch_new_word_by_page(
    new_word_query: Annotated[NewWordQuery, Query()], request: Request
) -> Dict[str, Any]:
    new_word_page_result: PageResult = await new_word_service.fetch_new_word_by_page(
        new_word_query=new_word_query,
        request=request
    )
    return HttpResponse.success(new_word_page_result)

@new_word_router.get("/detail/{id}")
async def fetch_new_word_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    new_word_detail: NewWordDetail = await new_word_service.fetch_new_word_detail(id=id, request=request)
    return HttpResponse.success(new_word_detail)

@new_word_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=NewWordCreate, file_name="new_word_import_tpl")

@new_word_router.get("/export")
async def export_new_word_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await new_word_service.export_new_word_page(ids=ids, request=request)

@new_word_router.post("/create")
async def create_new_word(
    new_word_create: NewWordCreate, request: Request
) -> Dict[str, Any]:
    new_word: NewWordDO = await new_word_service.create_new_word(new_word_create=new_word_create, request=request)
    return HttpResponse.success(new_word.id)

@new_word_router.post("/batch-create")
async def batch_create_new_word(
    new_word_create_list: List[NewWordCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await new_word_service.batch_create_new_word(new_word_create_list=new_word_create_list, request=request)
    return HttpResponse.success(ids)

@new_word_router.post("/import")
async def import_new_word(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    new_word_create_list: List[NewWordCreate] = await new_word_service.import_new_word(file=file, request=request)
    return HttpResponse.success(new_word_create_list)

@new_word_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await new_word_service.remove_by_id(id=id)
    return HttpResponse.success()

@new_word_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await new_word_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@new_word_router.put("/modify")
async def modify(
    new_word_modify: NewWordModify, request: Request
) -> Dict[str, Any]:
    await new_word_service.modify_by_id(data=NewWordDO(**new_word_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@new_word_router.put("/batch-modify")
async def batch_modify(new_word_batch_modify: NewWordBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in new_word_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await new_word_service.batch_modify_by_ids(ids=new_word_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()