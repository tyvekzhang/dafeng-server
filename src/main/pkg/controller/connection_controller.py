"""Connection operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.pkg.common import result
from src.main.pkg.common.util.excel_util import export_excel
from src.main.pkg.mapper.connection_mapper import connectionMapper
from src.main.pkg.model.connection_model import ConnectionDO
from src.main.pkg.schema.connection_schema import (
    ConnectionAdd,
    ConnectionExport,
    ConnectionQueryForm,
    ConnectionModify,
)
from src.main.pkg.schema.user_schema import Ids
from src.main.pkg.service.connection_service import ConnectionService
from src.main.pkg.service.impl.connection_service_impl import ConnectionServiceImpl
from starlette.responses import StreamingResponse

connection_router = APIRouter()
connection_service: ConnectionService = ConnectionServiceImpl(mapper=connectionMapper)


@connection_router.post("/add")
async def add(
    data: ConnectionAdd,
) -> Dict:
    """
    Connection add.

    Args:
        data: Data required for add.

    Returns:
        BaseResponse with new connection's ID.
    """
    connection: ConnectionDO = await connection_service.save(
        record=ConnectionDO(**data.model_dump())
    )
    return result.success(data=connection.id)


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
    connection: ConnectionDO = await connection_service.save(record=data)
    return result.success(data=connection.id)


@connection_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for connection information.

    Returns:
        StreamingResponse with connection field
    """
    return await export_excel(
        schema=ConnectionExport, file_name="connection_import_template"
    )


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


@connection_router.get("/connections")
async def connections(
    connection_filter_form: Annotated[ConnectionQueryForm, Query()],
) -> Dict:
    """
    Filter connections with pagination.

    Args:
        connection_filter_form: Pagination and filter info to query

    Returns:
        ConnectionQuery list and total count.
    """
    records, total_count = await connection_service.retrieve_ordered_records(
        data=connection_filter_form
    )
    return result.success(data={"records": records, "total_count": total_count})


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
    await connection_service.modify_by_id(
        record=ConnectionDO(**data.model_dump(exclude_unset=True))
    )
    return result.success()


@connection_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: ConnectionModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await connection_service.batch_modify_by_ids(ids=ids.ids, record=cleaned_data)
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
