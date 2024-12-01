"""GenTableColumn operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.common import result
from src.main.app.common.result import ResponseBase
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.gen_table_column_mapper import genTableColumnMapper
from src.main.app.model.gen_table_field_model import GenTableColumnDO
from src.main.app.schema.common_schema import PaginationResponse
from src.main.app.schema.gen_table_column_schema import (
    GenTableColumnAdd,
    GenTableColumnExport,
    GenTableColumnQueryForm,
    GenTableColumnModify,
    GenTableColumnQuery,
)
from src.main.app.schema.user_schema import Ids
from src.main.app.service.gen_table_column_service import GenTableColumnService
from src.main.app.service.impl.gen_table_column_service_impl import GenTableColumnServiceImpl
from starlette.responses import StreamingResponse

gen_table_column_router = APIRouter()
gen_table_column_service: GenTableColumnService = GenTableColumnServiceImpl(mapper=genTableColumnMapper)


@gen_table_column_router.post("/add")
async def add_gen_table_column(
    gen_table_column_add: GenTableColumnAdd,
) -> ResponseBase[int]:
    """
    GenTableColumn add.

    Args:
        gen_table_column_add: Data required for add.

    Returns:
        BaseResponse with new gen_table_column's ID.
    """
    gen_table_column: GenTableColumnDO = await gen_table_column_service.save(data=GenTableColumnDO(**gen_table_column_add.model_dump()))
    return ResponseBase(data=gen_table_column.id)


@gen_table_column_router.get("/gen_table_columns")
async def list_gen_table_columns(
    gen_table_column_query: Annotated[GenTableColumnQuery, Query()],
) -> ResponseBase[PaginationResponse]:
    """
    Filter gen_table_columns with pagination.

    Args:
        gen_table_column_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    records, total_count = await gen_table_column_service.list_gen_table_columns(data=gen_table_column_query)
    return ResponseBase(data=PaginationResponse(records=records, total_count=total_count))


@gen_table_column_router.post("/recover")
async def recover(
    data: GenTableColumnDO,
) -> Dict:
    """
    GenTableColumn recover that be deleted.

    Args:
        data: GenTableColumn recover data

    Returns:
        BaseResponse with gen_table_column's ID.
    """
    gen_table_column: GenTableColumnDO = await gen_table_column_service.save(data=data)
    return result.success(data=gen_table_column.id)


@gen_table_column_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for gen_table_column information.

    Returns:
        StreamingResponse with gen_table_column field
    """
    return await export_excel(schema=GenTableColumnExport, file_name="gen_table_column_import_template")


@gen_table_column_router.post("/import")
async def import_gen_table_column(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import gen_table_column information from a file.

    Args:
        file: The file containing gen_table_column information to import.

    Returns:
        Success result message
    """
    success_count = await gen_table_column_service.import_gen_table_column(file=file)
    return result.success(data=f"Success import count: {success_count}")


@gen_table_column_router.get("/export")
async def export(
    data: Annotated[GenTableColumnQueryForm, Query()],
) -> StreamingResponse:
    """
    Export gen_table_column information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with gen_table_column info
    """
    return await gen_table_column_service.export_gen_table_column(params=data)


@gen_table_column_router.put("/modify")
async def modify(
    data: GenTableColumnModify,
) -> Dict:
    """
    Update gen_table_column information.

    Args:
        data: Command containing updated gen_table_column info.

    Returns:
        Success result message
    """
    await gen_table_column_service.modify_by_id(data=GenTableColumnDO(**data.model_dump(exclude_unset=True)))
    return result.success()


@gen_table_column_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: GenTableColumnModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await gen_table_column_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
    return result.success()


@gen_table_column_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a gen_table_column by their ID.

    Args:
        id: GenTableColumn ID to remove.

    Returns:
        Success result message
    """
    await gen_table_column_service.remove_by_id(id=id)
    return result.success()


@gen_table_column_router.delete("/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete gen_table_columns by a list of IDs.

    Args:
        ids: List of gen_table_column IDs to delete.

    Returns:
        Success result message
    """
    await gen_table_column_service.batch_remove_by_ids(ids=ids)
    return result.success()
