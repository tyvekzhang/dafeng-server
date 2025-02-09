"""UserRole Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_user_role_model import UserRoleDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.sys_user_role_schema import UserRoleQuery, UserRoleDetail, UserRoleCreate, UserRoleAssign
from src.main.app.service.service_base import ServiceBase


class UserRoleService(ServiceBase[UserRoleDO], ABC):

    @abstractmethod
    async def fetch_user_role_by_page(self, *, user_role_query: UserRoleQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_user_role_detail(self, *, id: int, request: Request) -> Optional[UserRoleDetail]:...

    @abstractmethod
    async def export_user_role_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_user_role(self, *, user_role_create: UserRoleCreate, request: Request) -> UserRoleDO:...

    @abstractmethod
    async def batch_create_user_role(self, *, user_role_create_list: List[UserRoleCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_user_role(self, *, file: UploadFile, request: Request) -> List[UserRoleCreate]:...

    @abstractmethod
    async def assign_user_role(self, user_role_assign: UserRoleAssign, request):...