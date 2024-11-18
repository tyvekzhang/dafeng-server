"""Connection operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.common import result
from src.main.app.common.result import ResponseBase
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.schema.common_schema import PaginationResponse
from src.main.app.schema.connection_schema import (
    ConnectionAdd,
    ConnectionExport,
    ConnectionQueryForm,
    ConnectionModify,
    ConnectionQuery,
)
from src.main.app.schema.user_schema import Ids
from src.main.app.service.connection_service import ConnectionService
from src.main.app.service.impl.connection_service_impl import ConnectionServiceImpl
from starlette.responses import StreamingResponse

connection_router = APIRouter()
connection_service: ConnectionService = ConnectionServiceImpl(mapper=connectionMapper)


@connection_router.post("/add")
async def add_connection(
    connection_add: ConnectionAdd,
) -> ResponseBase[int]:
    """
    Connection add.

    Args:
        connection_add: Data required for add.

    Returns:
        BaseResponse with new connection's ID.
    """
    connection: ConnectionDO = await connection_service.save(data=ConnectionDO(**connection_add.model_dump()))
    return ResponseBase(data=connection.id)


@connection_router.get("/connections")
async def list_connections(
    connection_query: Annotated[ConnectionQuery, Query()],
) -> ResponseBase[PaginationResponse]:
    """
    Filter connections with pagination.

    Args:
        connection_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    records, total_count = await connection_service.list_connections(data=connection_query)
    return ResponseBase(data=PaginationResponse(records=records, total_count=total_count))


@connection_router.post("/recover")
async def recover(
    data: ConnectionDO,
) -> Dict:
    """
    Connection recover that be deleted.

    Args:
        data: Connection recover data

    Returns:
        BaseResponse with connection's ID.
    """
    connection: ConnectionDO = await connection_service.save(data=data)
    return result.success(data=connection.id)


@connection_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for connection information.

    Returns:
        StreamingResponse with connection field
    """
    return await export_excel(schema=ConnectionExport, file_name="connection_import_template")


@connection_router.post("/import")
async def import_connection(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import connection information from a file.

    Args:
        file: The file containing connection information to import.

    Returns:
        Success result message
    """
    success_count = await connection_service.import_connection(file=file)
    return result.success(data=f"Success import count: {success_count}")


@connection_router.get("/export")
async def export(
    data: Annotated[ConnectionQueryForm, Query()],
) -> StreamingResponse:
    """
    Export connection information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with connection info
    """
    return await connection_service.export_connection(params=data)


@connection_router.put("/modify")
async def modify(
    data: ConnectionModify,
) -> Dict:
    """
    Update connection information.

    Args:
        data: Command containing updated connection info.

    Returns:
        Success result message
    """
    await connection_service.modify_by_id(data=ConnectionDO(**data.model_dump(exclude_unset=True)))
    return result.success()


@connection_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: ConnectionModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await connection_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
    return result.success()


@connection_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a connection by their ID.

    Args:
        id: Connection ID to remove.

    Returns:
        Success result message
    """
    await connection_service.remove_by_id(id=id)
    return result.success()


@connection_router.delete("/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete connections by a list of IDs.

    Args:
        ids: List of connection IDs to delete.

    Returns:
        Success result message
    """
    await connection_service.batch_remove_by_ids(ids=ids)
    return result.success()
