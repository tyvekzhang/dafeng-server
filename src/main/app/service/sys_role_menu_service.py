"""RoleMenu Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_role_menu_model import RoleMenuDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_menu_schema import RoleMenuQuery, RoleMenuDetail, RoleMenuCreate
from src.main.app.service.service_base import ServiceBase


class RoleMenuService(ServiceBase[RoleMenuDO], ABC):

    @abstractmethod
    async def fetch_role_menu_by_page(self, *, role_menu_query: RoleMenuQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_role_menu_detail(self, *, id: int, request: Request) -> Optional[RoleMenuDetail]:...

    @abstractmethod
    async def export_role_menu_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_role_menu(self, *, role_menu_create: RoleMenuCreate, request: Request) -> RoleMenuDO:...

    @abstractmethod
    async def batch_create_role_menu(self, *, role_menu_create_list: List[RoleMenuCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_role_menu(self, *, file: UploadFile, request: Request) -> List[RoleMenuCreate]:...