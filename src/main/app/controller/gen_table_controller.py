"""GenTable operation controller"""
from datetime import datetime
from io import BytesIO
from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.common import result
from src.main.app.common.result import ResponseBase
from src.main.app.common.util.excel_util import export_excel
from src.main.app.common.util.time_util import get_current_time, get_date_time
from src.main.app.mapper.gen_table_mapper import genTableMapper
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.common_schema import PaginationResponse
from src.main.app.schema.gen_table_schema import (
    GenTableAdd,
    GenTableExport,
    GenTableQueryForm,
    GenTableModify,
    GenTableQuery, TableImport,
)
from src.main.app.schema.user_schema import Ids
from src.main.app.service.gen_table_service import GenTableService
from src.main.app.service.impl.gen_table_service_impl import GenTableServiceImpl
from starlette.responses import StreamingResponse

gen_table_router = APIRouter()
gen_table_service: GenTableService = GenTableServiceImpl(mapper=genTableMapper)


@gen_table_router.post("/add")
async def add_gen_table(
    gen_table_add: GenTableAdd,
) -> ResponseBase[int]:
    """
    GenTable add.

    Args:
        gen_table_add: Data required for add.

    Returns:
        BaseResponse with new gen_table's ID.
    """
    gen_table: GenTableDO = await gen_table_service.save(data=GenTableDO(**gen_table_add.model_dump()))
    return ResponseBase(data=gen_table.id)


@gen_table_router.get("/list")
async def list_gen_tables(
    gen_table_query: Annotated[GenTableQuery, Query()],
) -> ResponseBase[PaginationResponse]:
    """
    Filter gen_tables with pagination.

    Args:
        gen_table_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    records, total_count = await gen_table_service.list_gen_tables(data=gen_table_query)
    return ResponseBase(data=PaginationResponse(records=records, total_count=total_count))


@gen_table_router.post("/recover")
async def recover(
    data: GenTableDO,
) -> Dict:
    """
    GenTable recover that be deleted.

    Args:
        data: GenTable recover data

    Returns:
        BaseResponse with gen_table's ID.
    """
    gen_table: GenTableDO = await gen_table_service.save(data=data)
    return result.success(data=gen_table.id)


@gen_table_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for gen_table information.

    Returns:
        StreamingResponse with gen_table field
    """
    return await export_excel(schema=GenTableExport, file_name="gen_table_import_template")


@gen_table_router.post("/import")
async def import_gen_table(
    table_import: TableImport
) -> Dict:
    await gen_table_service.import_gen_table(data=table_import)
    return result.success()

@gen_table_router.get("/preview/{table_id}")
async def preview_code(table_id: int) -> Dict:
    res = await gen_table_service.preview_code(table_id)
    return result.success(res)


@gen_table_router.get("/download/{table_id}")
async def preview_code(table_id: int) -> StreamingResponse:
    # 生成代码
    data = await gen_table_service.download_code(table_id)

    # 创建一个字节流
    mem = BytesIO(data)
    mem.seek(0)

    # 定义一个生成器函数来流式传输数据
    def iterfile():
        yield from mem

    # 创建响应
    response = StreamingResponse(iterfile(), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=generated_code_{get_date_time()}.zip"

    return response


@gen_table_router.get("/export")
async def export(
    data: Annotated[GenTableQueryForm, Query()],
) -> StreamingResponse:
    """
    Export gen_table information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with gen_table info
    """
    return await gen_table_service.export_gen_table(params=data)


@gen_table_router.put("/modify")
async def modify(
    data: GenTableModify,
) -> Dict:
    """
    Update gen_table information.

    Args:
        data: Command containing updated gen_table info.

    Returns:
        Success result message
    """
    await gen_table_service.modify_by_id(data=GenTableDO(**data.model_dump(exclude_unset=True)))
    return result.success()


@gen_table_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: GenTableModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await gen_table_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
    return result.success()


@gen_table_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a gen_table by their ID.

    Args:
        id: GenTable ID to remove.

    Returns:
        Success result message
    """
    await gen_table_service.remove_by_id(id=id)
    return result.success()


@gen_table_router.delete("/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete gen_tables by a list of IDs.

    Args:
        ids: List of gen_table IDs to delete.

    Returns:
        Success result message
    """
    await gen_table_service.batch_remove_by_ids(ids=ids)
    return result.success()
