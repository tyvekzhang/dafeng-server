"""NewWord Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.read_new_word_model import NewWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_new_word_schema import NewWordQuery, NewWordDetail, NewWordCreate
from src.main.app.service.service_base import ServiceBase


class NewWordService(ServiceBase[NewWordDO], ABC):

    @abstractmethod
    async def fetch_new_word_by_page(self, *, new_word_query: NewWordQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_new_word_detail(self, *, id: int, request: Request) -> Optional[NewWordDetail]:...

    @abstractmethod
    async def export_new_word_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_new_word(self, *, new_word_create: NewWordCreate, request: Request) -> NewWordDO:...

    @abstractmethod
    async def batch_create_new_word(self, *, new_word_create_list: List[NewWordCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_new_word(self, *, file: UploadFile, request: Request) -> List[NewWordCreate]:...