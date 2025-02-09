"""UserRole 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_user_role_mapper import userRoleMapper
from src.main.app.model.sys_user_role_model import UserRoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_user_role_schema import UserRoleQuery, UserRoleModify, UserRoleCreate, \
    UserRoleBatchModify, UserRoleDetail, UserRoleAssign
from src.main.app.service.impl.sys_user_role_service_impl import UserRoleServiceImpl
from src.main.app.service.sys_user_role_service import UserRoleService

user_role_router = APIRouter()
user_role_service: UserRoleService = UserRoleServiceImpl(mapper=userRoleMapper)

@user_role_router.get("/page")
async def fetch_user_role_by_page(
    user_role_query: Annotated[UserRoleQuery, Query()], request: Request
) -> Dict[str, Any]:
    user_role_page_result: PageResult = await user_role_service.fetch_user_role_by_page(
        user_role_query=user_role_query,
        request=request
    )
    return HttpResponse.success(user_role_page_result)

@user_role_router.get("/detail/{id}")
async def fetch_user_role_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    user_role_detail: UserRoleDetail = await user_role_service.fetch_user_role_detail(id=id, request=request)
    return HttpResponse.success(user_role_detail)

@user_role_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=UserRoleCreate, file_name="user_role_import_tpl")

@user_role_router.get("/export")
async def export_user_role_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await user_role_service.export_user_role_page(ids=ids, request=request)

@user_role_router.post("/create")
async def create_user_role(
    user_role_create: UserRoleCreate, request: Request
) -> Dict[str, Any]:
    user_role: UserRoleDO = await user_role_service.create_user_role(user_role_create=user_role_create, request=request)
    return HttpResponse.success(user_role.id)

@user_role_router.post("/assign")
async def assign_user_role(
    user_role_assign: UserRoleAssign, request: Request
) -> Dict[str, Any]:
    await user_role_service.assign_user_role(user_role_assign=user_role_assign, request=request)
    return HttpResponse.success()

@user_role_router.post("/batch-create")
async def batch_create_user_role(
    user_role_create_list: List[UserRoleCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await user_role_service.batch_create_user_role(user_role_create_list=user_role_create_list, request=request)
    return HttpResponse.success(ids)

@user_role_router.post("/import")
async def import_user_role(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    user_role_create_list: List[UserRoleCreate] = await user_role_service.import_user_role(file=file, request=request)
    return HttpResponse.success(user_role_create_list)

@user_role_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await user_role_service.remove_by_id(id=id)
    return HttpResponse.success()

@user_role_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await user_role_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@user_role_router.put("/modify")
async def modify(
    user_role_modify: UserRoleModify, request: Request
) -> Dict[str, Any]:
    await user_role_service.modify_by_id(data=UserRoleDO(**user_role_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@user_role_router.put("/batch-modify")
async def batch_modify(user_role_batch_modify: UserRoleBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in user_role_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await user_role_service.batch_modify_by_ids(ids=user_role_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()