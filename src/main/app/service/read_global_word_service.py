"""GlobalWord Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.read_global_word_model import GlobalWordDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.read_global_word_schema import GlobalWordQuery, GlobalWordDetail, GlobalWordCreate
from src.main.app.service.service_base import ServiceBase


class GlobalWordService(ServiceBase[GlobalWordDO], ABC):

    @abstractmethod
    async def fetch_global_word_by_page(self, *, global_word_query: GlobalWordQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_global_word_detail(self, *, id: int, request: Request) -> Optional[GlobalWordDetail]:...

    @abstractmethod
    async def export_global_word_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_global_word(self, *, global_word_create: GlobalWordCreate, request: Request) -> GlobalWordDO:...

    @abstractmethod
    async def batch_create_global_word(self, *, global_word_create_list: List[GlobalWordCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_global_word(self, *, file: UploadFile, request: Request) -> List[GlobalWordCreate]:...