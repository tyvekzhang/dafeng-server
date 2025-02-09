"""RoleMenu 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_role_menu_mapper import roleMenuMapper
from src.main.app.model.sys_role_menu_model import RoleMenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_menu_schema import RoleMenuQuery, RoleMenuModify, RoleMenuCreate, \
    RoleMenuBatchModify, RoleMenuDetail
from src.main.app.service.impl.sys_role_menu_service_impl import RoleMenuServiceImpl
from src.main.app.service.sys_role_menu_service import RoleMenuService

role_menu_router = APIRouter()
role_menu_service: RoleMenuService = RoleMenuServiceImpl(mapper=roleMenuMapper)

@role_menu_router.get("/page")
async def fetch_role_menu_by_page(
    role_menu_query: Annotated[RoleMenuQuery, Query()], request: Request
) -> Dict[str, Any]:
    role_menu_page_result: PageResult = await role_menu_service.fetch_role_menu_by_page(
        role_menu_query=role_menu_query,
        request=request
    )
    return HttpResponse.success(role_menu_page_result)

@role_menu_router.get("/detail/{id}")
async def fetch_role_menu_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    role_menu_detail: RoleMenuDetail = await role_menu_service.fetch_role_menu_detail(id=id, request=request)
    return HttpResponse.success(role_menu_detail)

@role_menu_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=RoleMenuCreate, file_name="role_menu_import_tpl")

@role_menu_router.get("/export")
async def export_role_menu_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await role_menu_service.export_role_menu_page(ids=ids, request=request)

@role_menu_router.post("/create")
async def create_role_menu(
    role_menu_create: RoleMenuCreate, request: Request
) -> Dict[str, Any]:
    role_menu: RoleMenuDO = await role_menu_service.create_role_menu(role_menu_create=role_menu_create, request=request)
    return HttpResponse.success(role_menu.id)

@role_menu_router.post("/batch-create")
async def batch_create_role_menu(
    role_menu_create_list: List[RoleMenuCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await role_menu_service.batch_create_role_menu(role_menu_create_list=role_menu_create_list, request=request)
    return HttpResponse.success(ids)

@role_menu_router.post("/import")
async def import_role_menu(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    role_menu_create_list: List[RoleMenuCreate] = await role_menu_service.import_role_menu(file=file, request=request)
    return HttpResponse.success(role_menu_create_list)

@role_menu_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await role_menu_service.remove_by_id(id=id)
    return HttpResponse.success()

@role_menu_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await role_menu_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@role_menu_router.put("/modify")
async def modify(
    role_menu_modify: RoleMenuModify, request: Request
) -> Dict[str, Any]:
    await role_menu_service.modify_by_id(data=RoleMenuDO(**role_menu_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@role_menu_router.put("/batch-modify")
async def batch_modify(role_menu_batch_modify: RoleMenuBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in role_menu_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await role_menu_service.batch_modify_by_ids(ids=role_menu_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()