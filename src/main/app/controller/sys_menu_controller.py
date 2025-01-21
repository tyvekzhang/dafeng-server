"""Menu 前端控制器"""

from __future__ import annotations
from typing import Dict, Annotated, List, Any, Union
from fastapi import APIRouter, Query, UploadFile, Form, Request
from starlette.responses import StreamingResponse
from src.main.app.common.schema.response_schema import HttpResponse
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.sys_menu_mapper import menuMapper
from src.main.app.model.sys_menu_model import MenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_menu_schema import MenuQuery, MenuModify, MenuCreate, \
    MenuBatchModify, MenuDetail
from src.main.app.service.impl.sys_menu_service_impl import MenuServiceImpl
from src.main.app.service.sys_menu_service import MenuService

menu_router = APIRouter()
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)

@menu_router.get("/page")
async def fetch_menu_by_page(
    menu_query: Annotated[MenuQuery, Query()], request: Request
) -> Dict[str, Any]:
    menu_page_result: PageResult = await menu_service.fetch_menu_by_page(
        menu_query=menu_query,
        request=request
    )
    return HttpResponse.success(menu_page_result)

@menu_router.get("/detail/{id}")
async def fetch_menu_detail(
    id: int, request: Request
) -> Dict[str, Any]:
    menu_detail: MenuDetail = await menu_service.fetch_menu_detail(id=id, request=request)
    return HttpResponse.success(menu_detail)

@menu_router.get("/export-template")
async def export_template(request: Request) -> StreamingResponse:
    return await export_excel(schema=MenuCreate, file_name="menu_import_tpl")

@menu_router.get("/export")
async def export_menu_page(
    request: Request, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await menu_service.export_menu_page(ids=ids, request=request)

@menu_router.post("/create")
async def create_menu(
    menu_create: MenuCreate, request: Request
) -> Dict[str, Any]:
    menu: MenuDO = await menu_service.create_menu(menu_create=menu_create, request=request)
    return HttpResponse.success(menu.id)

@menu_router.post("/batch-create")
async def batch_create_menu(
    menu_create_list: List[MenuCreate], request: Request
) -> Dict[str, Any]:
    ids: List[int] = await menu_service.batch_create_menu(menu_create_list=menu_create_list, request=request)
    return HttpResponse.success(ids)

@menu_router.post("/import")
async def import_menu(
    request: Request, file: UploadFile = Form()
) -> Dict[str, Any]:
    menu_create_list: List[MenuCreate] = await menu_service.import_menu(file=file, request=request)
    return HttpResponse.success(menu_create_list)

@menu_router.delete("/remove/{id}")
async def remove(
    id: int, request: Request
) -> Dict[str, Any]:
    await menu_service.remove_by_id(id=id)
    return HttpResponse.success()

@menu_router.delete("/batch-remove")
async def batch_remove(
    request: Request, ids: List[int] = Query(...),
) -> Dict[str, Any]:
    await menu_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()

@menu_router.put("/modify")
async def modify(
    menu_modify: MenuModify, request: Request
) -> Dict[str, Any]:
    await menu_service.modify_by_id(data=MenuDO(**menu_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()

@menu_router.put("/batch-modify")
async def batch_modify(menu_batch_modify: MenuBatchModify, request: Request) -> Dict[str, Any]:
    cleaned_data = {k: v for k, v in menu_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await menu_service.batch_modify_by_ids(ids=menu_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()