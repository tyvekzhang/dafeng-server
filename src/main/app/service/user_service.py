"""User domain service interface"""

from abc import ABC, abstractmethod
from starlette.responses import StreamingResponse
from fastapi import UploadFile

from src.main.app.schema.common_schema import Token
from src.main.app.schema.user_schema import LoginCmd, UserQuery, UserFilterForm, UserAdd
from src.main.app.service.service_base import ServiceBase
from src.main.app.model.user_model import UserDO


class UserService(ServiceBase[UserDO], ABC):
    @abstractmethod
    async def add(self, *, data: UserAdd) -> UserDO: ...

    @abstractmethod
    async def login(self, *, login_cmd: LoginCmd) -> Token: ...

    @abstractmethod
    async def find_by_id(self, *, id: int) -> UserQuery: ...

    @abstractmethod
    async def generate_tokens(self, user_id: int) -> Token: ...

    @abstractmethod
    async def users(self, data: UserFilterForm) -> tuple[list[UserQuery], int]: ...

    @abstractmethod
    async def export_user(self, *, params: UserFilterForm, file_name: str) -> StreamingResponse: ...

    @abstractmethod
    async def import_user(self, *, file: UploadFile) -> int: ...
