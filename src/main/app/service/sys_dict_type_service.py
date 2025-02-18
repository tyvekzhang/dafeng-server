"""DictType Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_dict_type_model import DictTypeDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_dict_type_schema import DictTypeQuery, DictTypeDetail, DictTypeCreate
from src.main.app.service.service_base import ServiceBase


class DictTypeService(ServiceBase[DictTypeDO], ABC):

    @abstractmethod
    async def fetch_dict_type_by_page(self, *, dict_type_query: DictTypeQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_dict_type_detail(self, *, id: int, request: Request) -> Optional[DictTypeDetail]:...

    @abstractmethod
    async def export_dict_type_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_dict_type(self, *, dict_type_create: DictTypeCreate, request: Request) -> DictTypeDO:...

    @abstractmethod
    async def batch_create_dict_type(self, *, dict_type_create_list: List[DictTypeCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_dict_type(self, *, file: UploadFile, request: Request) -> List[DictTypeCreate]:...