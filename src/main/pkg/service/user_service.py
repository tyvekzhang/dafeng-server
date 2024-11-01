"""User domain service interface"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union

from src.main.pkg.schema.common_schema import Token
from src.main.pkg.schema.user_schema import LoginCmd, UserQuery
from src.main.pkg.service.base_service import Service
from src.main.pkg.type.user_do import UserDO


class UserService(Service[UserDO], ABC):
    @abstractmethod
    async def register(self, *, user_create_cmd) -> UserDO: ...

    @abstractmethod
    async def login(self, *, login_cmd: LoginCmd) -> Token: ...

    @abstractmethod
    async def find_by_id(self, *, id: int) -> UserQuery: ...

    @abstractmethod
    async def generate_tokens(self, user_id: int) -> Token: ...

    @abstractmethod
    async def retrieve_user(
        self, *, page: int, size: int, **kwargs
    ) -> tuple[list[UserQuery], int]:...
