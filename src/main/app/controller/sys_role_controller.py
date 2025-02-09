"""Role 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_role_mapper import roleMapper
from src.main.app.model.sys_role_model import RoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_schema import RoleQuery, RoleModify, RoleCreate, \
    RoleBatchModify, RoleDetail
from src.main.app.service.impl.sys_role_service_impl import RoleServiceImpl
from src.main.app.service.sys_role_service import RoleService

role_router = APIRouter()
role_service: RoleService = RoleServiceImpl(mapper=roleMapper)

@role_router.get("/page")
async def fetch_role_by_page(
    role_query: Annotated[RoleQuery, Query()], request: Request
) -> Dict[str, Any]:
    role_page_result: PageResult = await role_service.fetch_role_by_page(
        role_query=role_query,
        request=request
    )
    return HttpResponse.success(role_page_result)

@role_router.get("/detail/{id}")
async def fetch_role_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    role_detail: RoleDetail = await role_service.fetch_role_detail(id=id, request=request)
    return HttpResponse.success(role_detail)

@role_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=RoleCreate, file_name="role_import_tpl")

@role_router.get("/export")
async def export_role_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await role_service.export_role_page(ids=ids, request=request)

@role_router.post("/create")
async def create_role(
    role_create: RoleCreate, request: Request
) -> Dict[str, Any]:
    print(role_create)
    role: RoleDO = await role_service.create_role(role_create=role_create, request=request)
    return HttpResponse.success(role.id)

@role_router.post("/batch-create")
async def batch_create_role(
    role_create_list: List[RoleCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await role_service.batch_create_role(role_create_list=role_create_list, request=request)
    return HttpResponse.success(ids)

@role_router.post("/import")
async def import_role(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    role_create_list: List[RoleCreate] = await role_service.import_role(file=file, request=request)
    return HttpResponse.success(role_create_list)

@role_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await role_service.remove_by_id(id=id)
    return HttpResponse.success()

@role_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await role_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@role_router.put("/modify")
async def modify(
    role_modify: RoleModify, request: Request
) -> Dict[str, Any]:
    await role_service.modify_by_id(data=RoleDO(**role_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@role_router.put("/batch-modify")
async def batch_modify(role_batch_modify: RoleBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in role_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await role_service.batch_modify_by_ids(ids=role_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()