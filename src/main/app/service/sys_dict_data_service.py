"""DictData Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_dict_data_model import DictDataDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_dict_data_schema import DictDataQuery, DictDataDetail, DictDataCreate
from src.main.app.service.service_base import ServiceBase


class DictDataService(ServiceBase[DictDataDO], ABC):

    @abstractmethod
    async def fetch_dict_data_by_page(self, *, dict_data_query: DictDataQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_dict_data_detail(self, *, id: int, request: Request) -> Optional[DictDataDetail]:...

    @abstractmethod
    async def export_dict_data_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_dict_data(self, *, dict_data_create: DictDataCreate, request: Request) -> DictDataDO:...

    @abstractmethod
    async def batch_create_dict_data(self, *, dict_data_create_list: List[DictDataCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_dict_data(self, *, file: UploadFile, request: Request) -> List[DictDataCreate]:...

    @abstractmethod
    async def get_all_data(self, request: Request):...