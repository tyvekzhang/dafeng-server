"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Tuple, Union, Dict

T = TypeVar("T", bound=Any)


class Service(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, record: T) -> T: ...

    @abstractmethod
    async def batch_save(self, *, records: List[T]) -> bool: ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: Union[int, str]) -> T: ...

    @abstractmethod
    async def retrieve_by_ids(self, *, ids: Union[List[int], List[str]]) -> List[T]: ...

    @abstractmethod
    async def retrieve_records(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]: ...

    @abstractmethod
    async def retrieve_ordered_records(
        self, *, page: int, size: int, order_by: str, sort_order: str, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]: ...

    @abstractmethod
    async def modify_by_id(self, *, record: T) -> bool: ...

    @abstractmethod
    async def batch_modify_by_ids(
        self, *, ids: Union[List[int], List[str]], record: Dict, db_session: Any = None
    ) -> bool: ...

    @abstractmethod
    async def remove_by_id(self, *, id: Union[int, str]) -> bool: ...

    @abstractmethod
    async def batch_remove_by_ids(
        self, *, ids: Union[List[int], List[str]]
    ) -> bool: ...
