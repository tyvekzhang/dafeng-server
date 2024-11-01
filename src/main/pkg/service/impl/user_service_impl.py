"""User domain service impl"""

import http
from datetime import timedelta, datetime
from typing import Optional, List, Union, Tuple

from src.main.pkg.config.config import Config
from src.main.pkg.enums.enum import ResponseCode, TokenTypeEnum
from src.main.pkg.exception.exception import ServiceException, SystemException
from src.main.pkg.mapper.user_mapper import UserMapper
from src.main.pkg.schema.common_schema import Token
from src.main.pkg.schema.user_schema import UserCreateCmd, LoginCmd, UserQuery
from src.main.pkg.service.impl.base_service_impl import ServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO
from src.main.pkg.util import security_util
from src.main.pkg.util.security_util import get_password_hash, verify_password


class UserServiceImpl(ServiceImpl[UserMapper, UserDO], UserService):
    """
    Implementation of the UserService interface.
    """

    def __init__(self, mapper: UserMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (UserMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def register(self, user_create_cmd: UserCreateCmd) -> UserDO:
        """
        Register a new user.

        Args:
            user_create_cmd (UserCreateCmd): The user creation command containing username and password.

        Returns:
            UserDO: The newly created user.
        """
        # user name duplicate verification
        user: UserDO = await self.mapper.get_user_by_username(
            username=user_create_cmd.username
        )
        if user is not None:
            raise ServiceException(
                ResponseCode.USER_NAME_EXISTS.code,
                ResponseCode.USER_NAME_EXISTS.msg,
            )
        # generate hash password
        user_create_cmd.password = get_password_hash(user_create_cmd.password)
        return await self.mapper.insert_record(record=user_create_cmd)

    async def generate_tokens(self, user_id: int) -> Token:
        config = Config()

        # generate access token
        access_token_expires = timedelta(
            minutes=config.security.access_token_expire_minutes
        )
        access_token = security_util.create_token(
            subject=user_id, token_type=TokenTypeEnum.access
        )

        # generate refresh token
        refresh_token_expires = timedelta(
            days=config.security.refresh_token_expire_days
        )
        refresh_token = security_util.create_token(
            subject=user_id,
            token_type=TokenTypeEnum.refresh,
            expires_delta=refresh_token_expires,
        )

        # 计算过期时间
        access_token_expires_at = int(
            (datetime.now() + access_token_expires).timestamp()
        )
        refresh_token_expires_at = int(
            (datetime.now() + refresh_token_expires).timestamp()
        )

        return Token(
            access_token=access_token,
            expired_at=access_token_expires_at,
            token_type=TokenTypeEnum.bearer,
            refresh_token=refresh_token,
            re_expired_at=refresh_token_expires_at,
        )

    async def login(self, login_cmd: LoginCmd) -> Token:
        """
        Perform login and return an access token and refresh token.

        Args:
            login_cmd (LoginCmd): The login command containing username and password.

        Returns:
            Token: The access token and refresh token.
        """
        # verify username and password
        username: str = login_cmd.username
        user_do: UserDO = await self.mapper.get_user_by_username(username=username)
        if user_do is None or not verify_password(login_cmd.password, user_do.password):
            raise SystemException(
                ResponseCode.AUTH_FAILED.code,
                ResponseCode.AUTH_FAILED.msg,
                status_code= ResponseCode.AUTH_FAILED.code,
            )
        return await self.generate_tokens(user_id=user_do.id)

    async def find_by_id(self, id: int) -> Optional[UserQuery]:
        """
        Retrieve a user by ID.

        Args:
            id (int): The user ID to retrieve.

        Returns:
            Optional[UserQuery]: The user query object if found, None otherwise.
        """
        user_do = await self.mapper.select_record_by_id(id=id)
        return UserQuery(**user_do.model_dump()) if user_do else None

    async def retrieve_user(
        self, page: int, size: int, **kwargs
    ) -> tuple[list[UserQuery], int]:
        """
        List users with pagination.

        Args:
            page (int): The page number.
            size (int): The page size.

        Returns:
            Optional[List[UserQuery]]: The list of users or None if no users are found.
        """
        results, total_count = await self.mapper.select_ordered_records(page=page, size=size, **kwargs)
        return [UserQuery(**user.model_dump()) for user in results], total_count
