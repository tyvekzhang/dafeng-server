"""User domain service interface"""

from abc import ABC, abstractmethod

from src.main.pkg.service.base_service import Service
from src.main.pkg.type.user_do import UserDO


class UserService(Service[UserDO], ABC):
    @abstractmethod
    async def register(self, *, user_create_cmd) -> UserDO: ...
