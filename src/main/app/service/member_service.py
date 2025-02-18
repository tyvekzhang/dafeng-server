"""Member Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.member_model import MemberDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.member_schema import MemberQuery, MemberDetail, MemberCreate
from src.main.app.service.service_base import ServiceBase


class MemberService(ServiceBase[MemberDO], ABC):

    @abstractmethod
    async def fetch_member_by_page(self, *, member_query: MemberQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_member_detail(self, *, id: int, request: Request) -> Optional[MemberDetail]:...

    @abstractmethod
    async def export_member_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_member(self, *, member_create: MemberCreate, request: Request) -> MemberDO:...

    @abstractmethod
    async def batch_create_member(self, *, member_create_list: List[MemberCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_member(self, *, file: UploadFile, request: Request) -> List[MemberCreate]:...