"""Table operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.common import result
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.table_model import TableDO
from src.main.app.schema.table_schema import (
    TableAdd,
    TableExport,
    TableQueryForm,
    TableModify,
)
from src.main.app.schema.user_schema import Ids
from src.main.app.service.table_service import TableService
from src.main.app.service.impl.table_service_impl import TableServiceImpl
from starlette.responses import StreamingResponse

table_router = APIRouter()
table_service: TableService = TableServiceImpl(mapper=tableMapper)


@table_router.post("/add")
async def add(
    data: TableAdd,
) -> Dict:
    """
    Table add.

    Args:
        data: Data required for add.

    Returns:
        BaseResponse with new table's ID.
    """
    table: TableDO = await table_service.save(record=TableDO(**data.model_dump()))
    return result.success(data=table.id)


@table_router.post("/recover")
async def recover(
    data: TableDO,
) -> Dict:
    """
    Table recover that be deleted.

    Args:
        data: Table recover data

    Returns:
        BaseResponse with table's ID.
    """
    table: TableDO = await table_service.save(record=data)
    return result.success(data=table.id)


@table_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for table information.

    Returns:
        StreamingResponse with table field
    """
    return await export_excel(schema=TableExport, file_name="table_import_template")


@table_router.post("/import")
async def import_table(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import table information from a file.

    Args:
        file: The file containing table information to import.

    Returns:
        Success result message
    """
    success_count = await table_service.import_table(file=file)
    return result.success(data=f"Success import count: {success_count}")


@table_router.get("/tables")
async def tables(
    table_filter_form: Annotated[TableQueryForm, Query()],
) -> Dict:
    """
    Filter tables with pagination.

    Args:
        table_filter_form: Pagination and filter info to query

    Returns:
        TableQuery list and total count.
    """
    records, total_count = await table_service.retrieve_ordered_records(
        data=table_filter_form
    )
    return result.success(data={"records": records, "total_count": total_count})


@table_router.get("/export")
async def export(
    data: Annotated[TableQueryForm, Query()],
) -> StreamingResponse:
    """
    Export table information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with table info
    """
    return await table_service.export_table(params=data)


@table_router.put("/modify")
async def modify(
    data: TableModify,
) -> Dict:
    """
    Update table information.

    Args:
        data: Command containing updated table info.

    Returns:
        Success result message
    """
    await table_service.modify_by_id(
        record=TableDO(**data.model_dump(exclude_unset=True))
    )
    return result.success()


@table_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: TableModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await table_service.batch_modify_by_ids(ids=ids.ids, record=cleaned_data)
    return result.success()


@table_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a table by their ID.

    Args:
        id: Table ID to remove.

    Returns:
        Success result message
    """
    await table_service.remove_by_id(id=id)
    return result.success()


@table_router.delete("/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete tables by a list of IDs.

    Args:
        ids: List of table IDs to delete.

    Returns:
        Success result message
    """
    await table_service.batch_remove_by_ids(ids=ids)
    return result.success()
