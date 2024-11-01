"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Type, Tuple

from src.main.pkg.enums.enum import ResponseCode
from src.main.pkg.exception.exception import SystemException
from src.main.pkg.mapper.base_mapper import BaseMapper
from src.main.pkg.service.base_service import Service

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=BaseMapper)


class ServiceImpl(Generic[M, T], Service[T]):
    def __init__(self, mapper: Type[M]):
        self.mapper = mapper

    async def save(self, *, record: T) -> T:
        return await self.mapper.insert_record(record=record)

    async def batch_save(self, *, records: List[T]) -> bool:
        await self.mapper.batch_insert_records(records=records)
        return True

    async def retrieve_by_id(self, *, id: T) -> T:
        return await self.mapper.select_record_by_id(id=id)

    async def retrieve_by_ids(self, *, ids: List[T]) -> List[T]:
        return await self.mapper.select_records_by_ids(ids=ids)

    async def retrieve_records(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[Any],
        int,
    ]:
        return await self.mapper.select_records(page=page, size=size, **kwargs)

    async def retrieve_ordered_records(
        self,
        *,
        page: int,
        size: int,
        order_by: T = None,
        sort_order: T = None,
        **kwargs,
    ) -> Tuple[
        List[Any],
        int,
    ]:
        return await self.mapper.select_ordered_records(
            page=page, size=size, order_by=order_by, sort_order=sort_order, **kwargs
        )

    async def modify_by_id(self, *, record: T) -> bool:
        affect_row: int = await self.mapper.update_record_by_id(record=record)
        if affect_row != 1:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def batch_modify_by_ids(
        self, *, ids: List[Any], record: dict, db_session: Any = None
    ) -> bool:
        affect_row: int = await self.mapper.batch_update_records_by_ids(
            ids=ids, record=record
        )
        if len(ids) != affect_row:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def remove_by_id(self, *, id: T) -> bool:
        affect_row: int = await self.mapper.delete_record_by_id(id=id)
        if affect_row != 1:
            raise SystemException(
                ResponseCode.PARAMETER_ERROR.code,
                ResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def batch_remove_by_ids(self, *, ids: List[Any]) -> bool:
        affect_row: int = await self.mapper.batch_delete_records_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise SystemException(
                ResponseCode.DELETE_PARAMETER_ERROR.code,
                ResponseCode.DELETE_PARAMETER_ERROR.msg,
            )
        return True
