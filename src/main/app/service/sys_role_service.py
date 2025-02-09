"""Role Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_role_model import RoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_role_schema import RoleQuery, RoleDetail, RoleCreate
from src.main.app.service.service_base import ServiceBase


class RoleService(ServiceBase[RoleDO], ABC):

    @abstractmethod
    async def fetch_role_by_page(self, *, role_query: RoleQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_role_detail(self, *, id: int, request: Request) -> Optional[RoleDetail]:...

    @abstractmethod
    async def export_role_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_role(self, *, role_create: RoleCreate, request: Request) -> RoleDO:...

    @abstractmethod
    async def batch_create_role(self, *, role_create_list: List[RoleCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_role(self, *, file: UploadFile, request: Request) -> List[RoleCreate]:...