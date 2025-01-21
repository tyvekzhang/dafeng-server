"""Menu Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_menu_model import MenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_menu_schema import MenuQuery, MenuDetail, MenuCreate
from src.main.app.service.service_base import ServiceBase


class MenuService(ServiceBase[MenuDO], ABC):

    @abstractmethod
    async def fetch_menu_by_page(self, *, menu_query: MenuQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_menu_detail(self, *, id: int, request: Request) -> Optional[MenuDetail]:...

    @abstractmethod
    async def export_menu_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_menu(self, *, menu_create: MenuCreate, request: Request) -> MenuDO:...

    @abstractmethod
    async def batch_create_menu(self, *, menu_create_list: List[MenuCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_menu(self, *, file: UploadFile, request: Request) -> List[MenuCreate]:...