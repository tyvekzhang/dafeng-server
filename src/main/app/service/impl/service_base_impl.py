"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Tuple, Union, Dict

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.model_base import ModelBase

T = TypeVar("T", bound=ModelBase)
M = TypeVar("M", bound=SqlModelMapper)


class ServiceBaseImpl(Generic[M, T], ServiceBase[T]):
    def __init__(self, mapper: M):
        self.mapper = mapper

    async def save(self, *, record: T) -> T:
        return await self.mapper.insert(record=record)

    async def batch_save(self, *, records: List[T]) -> int:
        return await self.mapper.batch_insert(records=records)

    async def retrieve_by_id(self, *, id: Union[int, str]) -> T:
        return await self.mapper.select_by_id(id=id)

    async def retrieve_by_ids(self, *, ids: Union[List[int], List[str]]) -> List[T]:
        return await self.mapper.select_by_ids(ids=ids)

    async def retrieve_records(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_pagination(page=page, size=size, **kwargs)

    async def retrieve_ordered_records(
        self, *, page: int, size: int, order_by: str, sort_order: str, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_ordered_pagination(
            page=page, size=size, order_by=order_by, sort_order=sort_order, **kwargs
        )

    async def modify_by_id(self, *, record: T) -> None:
        affect_row: int = await self.mapper.update_by_id(record=record)
        if affect_row != 1:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )

    async def batch_modify_by_ids(
        self, *, ids: Union[List[int], List[str]], record: Dict, db_session: Any = None
    ) -> None:
        affect_row: int = await self.mapper.batch_update_by_ids(ids=ids, record=record)
        if len(ids) != affect_row:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )

    async def remove_by_id(self, *, id: Union[int, str]) -> None:
        affect_row: int = await self.mapper.delete_by_id(id=id)
        if affect_row != 1:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )

    async def batch_remove_by_ids(self, *, ids: Union[List[int], List[str]]) -> None:
        affect_row: int = await self.mapper.batch_delete_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )