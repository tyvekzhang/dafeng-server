"""Member 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.member_mapper import memberMapper
from src.main.app.model.member_model import MemberDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.member_schema import MemberQuery, MemberModify, MemberCreate, \
    MemberBatchModify, MemberDetail
from src.main.app.service.impl.member_service_impl import MemberServiceImpl
from src.main.app.service.member_service import MemberService

member_router = APIRouter()
member_service: MemberService = MemberServiceImpl(mapper=memberMapper)

@member_router.get("/page")
async def fetch_member_by_page(
    member_query: Annotated[MemberQuery, Query()], request: Request
) -> Dict[str, Any]:
    member_page_result: PageResult = await member_service.fetch_member_by_page(
        member_query=member_query,
        request=request
    )
    return HttpResponse.success(member_page_result)

@member_router.get("/detail/{id}")
async def fetch_member_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    member_detail: MemberDetail = await member_service.fetch_member_detail(id=id, request=request)
    return HttpResponse.success(member_detail)

@member_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=MemberCreate, file_name="member_import_tpl")

@member_router.get("/export")
async def export_member_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await member_service.export_member_page(ids=ids, request=request)

@member_router.post("/create")
async def create_member(
    member_create: MemberCreate, request: Request
) -> Dict[str, Any]:
    member: MemberDO = await member_service.create_member(member_create=member_create, request=request)
    return HttpResponse.success(member.id)

@member_router.post("/batch-create")
async def batch_create_member(
    member_create_list: List[MemberCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await member_service.batch_create_member(member_create_list=member_create_list, request=request)
    return HttpResponse.success(ids)

@member_router.post("/import")
async def import_member(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    member_create_list: List[MemberCreate] = await member_service.import_member(file=file, request=request)
    return HttpResponse.success(member_create_list)

@member_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await member_service.remove_by_id(id=id)
    return HttpResponse.success()

@member_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await member_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@member_router.put("/modify")
async def modify(
    member_modify: MemberModify, request: Request
) -> Dict[str, Any]:
    await member_service.modify_by_id(data=MemberDO(**member_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@member_router.put("/batch-modify")
async def batch_modify(member_batch_modify: MemberBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in member_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await member_service.batch_modify_by_ids(ids=member_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()