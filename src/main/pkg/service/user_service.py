"""User domain service interface"""

from abc import ABC, abstractmethod
from starlette.responses import StreamingResponse

from src.main.pkg.schema.common_schema import Token, BasePage
from src.main.pkg.schema.user_schema import LoginCmd, UserQuery, UserFilterForm
from src.main.pkg.service.base_service import Service
from src.main.pkg.type.user_do import UserDO


class UserService(Service[UserDO], ABC):
    @abstractmethod
    async def register(self, *, user_create) -> UserDO: ...

    @abstractmethod
    async def login(self, *, login_cmd: LoginCmd) -> Token: ...

    @abstractmethod
    async def find_by_id(self, *, id: int) -> UserQuery: ...

    @abstractmethod
    async def generate_tokens(self, user_id: int) -> Token: ...

    @abstractmethod
    async def retrieve_user(self, user_filter_form: UserFilterForm) -> tuple[list[UserQuery], int]:...

    @abstractmethod
    async def export_user(
        self, *, params: BasePage, file_name: str
    ) -> StreamingResponse: ...
