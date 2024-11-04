"""User domain service impl"""

import io
from datetime import timedelta, datetime
from starlette.responses import StreamingResponse
from fastapi import UploadFile
from typing import Optional, List
import pandas as pd

from src.main.pkg.config.config import Config
from src.main.pkg.enums.enum import ResponseCode, TokenTypeEnum
from src.main.pkg.exception.exception import ServiceException, SystemException
from src.main.pkg.mapper.user_mapper import UserMapper
from src.main.pkg.schema.common_schema import Token
from src.main.pkg.schema.user_schema import (
    UserCreate,
    LoginCmd,
    UserQuery,
    UserFilterForm,
)
from src.main.pkg.service.impl.base_service_impl import ServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO
from src.main.pkg.util import security_util
from src.main.pkg.util.excel_util import export_excel
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

    async def register(self, user_create: UserCreate) -> UserDO:
        """
        Register a new user.

        Args:
            user_create (UserCreate): The user creation command containing username and password.

        Returns:
            UserDO: The newly created user.
        """
        # user name duplicate verification
        user: UserDO = await self.mapper.get_user_by_username(
            username=user_create.username
        )
        if user is not None:
            raise ServiceException(
                ResponseCode.USER_NAME_EXISTS.code,
                ResponseCode.USER_NAME_EXISTS.msg,
            )
        # generate hash password
        user_create.password = get_password_hash(user_create.password)
        return await self.mapper.insert_record(record=user_create)

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
                status_code=ResponseCode.AUTH_FAILED.code,
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
        self, user_filter_form: UserFilterForm
    ) -> tuple[list[UserQuery], int]:
        status = user_filter_form.status
        username = user_filter_form.username
        nickname = user_filter_form.nickname
        create_time = user_filter_form.create_time
        filter_by = {}
        like = {}
        between = {}
        if status is not None:
            filter_by["status"] = status
        if username is not None and len(username) > 0:
            like["username"] = f"%{username}%"
        if nickname is not None and len(nickname) > 0:
            like["nickname"] = f"%{nickname}%"
        if create_time is not None and len(create_time) > 0:
            time_range = create_time.split(",")
            start_time = int(time_range[0])
            end_time = int(time_range[1])
            between["create_time"] = start_time, end_time
        results, total_count = await self.mapper.select_ordered_records(
            page=user_filter_form.page,
            size=user_filter_form.size,
            count=user_filter_form.count,
            filter_by=filter_by,
            like=like,
            between=between,
        )
        return [UserQuery(**user.model_dump()) for user in results], total_count

    async def export_user(
        self, params: UserFilterForm, file_name: str = "user"
    ) -> StreamingResponse:
        """
        Export user record to an Excel file.

        Args:
            params (Params): The query parameters for filtering users.
            file_name: File name for export

        Returns:
            StreamingResponse: The Excel file containing user record.
        """
        user_pages, _ = await self.retrieve_user(params)
        records = []
        for user in user_pages:
            records.append(UserQuery(**user.model_dump()))
        return await export_excel(
            schema=UserQuery, file_name=file_name, records=records
        )

    async def import_user(self, file: UploadFile):
        """
        Import user record from an Excel file.

        Args:
            file (UploadFile): The Excel file containing user record.
        """
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_records = import_df.to_dict(orient="records")
        if len(user_records) == 0:
            return
        for record in user_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_import_list = []
        user_name_list = []

        for user_record in user_records:
            user_import = UserDO(**user_record, exclude_unset=True)
            user_import.password = get_password_hash(user_import.password)
            user_import_list.append(user_import)
            user_name_list.append(user_import.username)
        await file.close()

        # Check if any usernames already exist
        existing_users: List[UserDO] = await self.mapper.get_user_by_usernames(
            usernames=user_name_list
        )

        if existing_users:
            existing_usernames = [user.username for user in existing_users]
            err_msg = ",".join(existing_usernames)
            raise SystemException(
                ResponseCode.USER_NAME_EXISTS.code,
                f"{ResponseCode.USER_NAME_EXISTS.msg}{err_msg}",
            )
        await self.mapper.batch_insert_records(records=user_import_list)
