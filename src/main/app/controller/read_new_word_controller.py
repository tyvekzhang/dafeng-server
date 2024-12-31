"""NewWord operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.common import result
from src.main.app.common.result import ResponseBase
from src.main.app.common.util.excel_util import export_excel
from src.main.app.mapper.read_new_word_mapper import newWordMapper
from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.common_schema import PaginationResponse
from src.main.app.schema.read_new_word_schema import NewWordAdd, NewWordQuery, NewWordQueryResponse, NewWordExport, \
    NewWordQueryForm, NewWordModify, NewWordCreate, NewWordBatchModify
from src.main.app.schema.user_schema import Ids
from starlette.responses import StreamingResponse

from src.main.app.service.impl.read_new_word_service_impl import NewWordServiceImpl
from src.main.app.service.read_new_word_service import NewWordService

new_word_router = APIRouter()
new_word_service: NewWordService = NewWordServiceImpl(mapper=newWordMapper)


@new_word_router.post("/create")
async def add_new_word(
    new_word_add: NewWordAdd,
) -> ResponseBase[int]:
    """
    NewWord add.

    Args:
        new_word_add: Data required for add.

    Returns:
        BaseResponse with new new_word's ID.
    """
    new_word: NewWordDO = await new_word_service.save(data=NewWordDO(**new_word_add.model_dump()))
    return ResponseBase(data=new_word.id)

@new_word_router.post("/batch-create")
async def batch_add_new_word(
    new_word_adds: List[NewWordCreate],
) -> Dict:
    """
    NewWord add.

    Args:
        new_word_add: Data required for add.

    Returns:
        BaseResponse with new new_word's ID.
    """
    ids = []
    for new_word_add in new_word_adds:
        new_word: NewWordDO = await new_word_service.save(data=NewWordDO(**new_word_add.model_dump()))
        ids.append(new_word.id)
    return result.success(data=ids)


@new_word_router.get("/page")
async def fetch_new_word_by_page(
    new_word_query: Annotated[NewWordQuery, Query()],
) -> ResponseBase[PaginationResponse]:
    """
    Filter new_words with pagination.

    Args:
        new_word_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    records, total = await new_word_service.fetch_new_word_by_page(new_word_query=new_word_query)
    return ResponseBase(data=PaginationResponse(records=records, total=total))


@new_word_router.get("/query/{new_word_id}")
async def query_new_words(
    new_word_id: int
) -> ResponseBase[NewWordQueryResponse]:
    record = await new_word_service.retrieve_by_id(id=new_word_id)
    if record is None:
        return ResponseBase(data=record)
    return ResponseBase(data=NewWordQueryResponse(**record.model_dump()))


@new_word_router.post("/recover")
async def recover(
    data: NewWordDO,
) -> Dict:
    """
    NewWord recover that be deleted.

    Args:
        data: NewWord recover data

    Returns:
        BaseResponse with new_word's ID.
    """
    new_word: NewWordDO = await new_word_service.save(data=data)
    return result.success(data=new_word.id)


@new_word_router.get("/export-template")
async def export_template() -> StreamingResponse:
    """
    Export a template for new_word information.

    Returns:
        StreamingResponse with new_word field
    """
    return await export_excel(schema=NewWordExport, file_name="new_word_import_template")


@new_word_router.post("/import")
async def import_new_word(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import new_word information from a file.

    Args:
        file: The file containing new_word information to import.

    Returns:
        Success result message
    """
    success_count = [NewWordCreate()]
    return result.success(data=success_count)


@new_word_router.get("/export")
async def export(
    data: Annotated[NewWordQueryForm, Query()],
) -> StreamingResponse:
    """
    Export new_word information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with new_word info
    """
    records = []
    for i in range(3):
        records.append(NewWordExport())
    return await export_excel(schema=NewWordExport, file_name="new_word_export.xlsx", records=records)


@new_word_router.put("/modify")
async def modify(
    data: NewWordModify,
) -> Dict:
    """
    Update new_word information.

    Args:
        data: Command containing updated new_word info.

    Returns:
        Success result message
    """
    await new_word_service.modify_by_id(data=NewWordDO(**data.model_dump(exclude_unset=True)))
    return result.success()


@new_word_router.put("/batch-modify")
async def batch_modify(data: NewWordBatchModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await new_word_service.batch_modify_by_ids(ids=data.ids, data=cleaned_data)
    return result.success()


@new_word_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a new_word by their ID.

    Args:
        id: NewWord ID to remove.

    Returns:
        Success result message
    """
    await new_word_service.remove_by_id(id=id)
    return result.success()


@new_word_router.delete("/batch-remove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete new_words by a list of IDs.

    Args:
        ids: List of new_word IDs to delete.

    Returns:
        Success result message
    """
    await new_word_service.batch_remove_by_ids(ids=ids)
    return result.success()
