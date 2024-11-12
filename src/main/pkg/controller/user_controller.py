"""User operation controller"""

import re
from typing import Dict, Annotated, List

from fastapi import APIRouter, Depends, Query, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse
from jwt import PyJWTError

from src.main.pkg.common.enums.enum import ResponseCode
from src.main.pkg.common.exception.exception import SystemException
from src.main.pkg.mapper.user_mapper import userMapper
from src.main.pkg.common import result
from src.main.pkg.schema.common_schema import Token, CurrentUser
from src.main.pkg.common.result import BaseResponse
from src.main.pkg.schema.user_schema import (
    UserAdd,
    LoginCmd,
    UserQuery,
    RefreshToken,
    UserUpdateCmd,
    UserFilterForm,
    UserExport,
    UserBatchUpdate,
    Ids,
)
from src.main.pkg.service.impl.user_service_impl import UserServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.model.user_model import UserDO
from src.main.pkg.common.util.excel_util import export_excel
from src.main.pkg.common.util.security_util import (
    get_current_user,
    is_token_valid,
    get_user_id,
    get_password_hash,
)

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)


@user_router.post("/add")
async def add(
    data: UserAdd,
) -> Dict:
    """
    User add.

    Args:
        data: Data required for add.

    Returns:
        BaseResponse with new user's ID.
    """
    user: UserDO = await user_service.add(data=data)
    return result.success(data=user.id)


@user_router.post("/login")
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Authenticates user and provides an access token.

    Args:
        data: Login credentials.

    Returns:
        Token object with access token.
    """
    login_cmd = LoginCmd(username=data.username, password=data.password)
    return await user_service.login(login_cmd=login_cmd)


@user_router.post("/refreshtoken")
async def refresh_tokens(data: RefreshToken):
    refresh_token = data.refresh_token
    if not is_token_valid(refresh_token):
        raise PyJWTError
    user_id: int = get_user_id(refresh_token)
    return await user_service.generate_tokens(user_id)


@user_router.get("/me")
async def me(
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[UserQuery]:
    """
    Retrieves the profile of the current user.

    Args:
        current_user: Currently authenticated user.

    Returns:
        BaseResponse with current user's profile information.
    """
    user: UserQuery = await user_service.find_by_id(id=current_user.id)
    return BaseResponse(data=user)


@user_router.post("/recover")
async def recover(
    data: UserDO,
) -> Dict:
    """
    User recover that be deleted.

    Args:
        data: User recover data

    Returns:
        BaseResponse with user's ID.
    """
    user: UserDO = await user_service.save(record=data)
    return result.success(data=user.id)


@user_router.get("/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for user information.

    Returns:
        StreamingResponse with user field
    """
    return await export_excel(schema=UserExport, file_name="user_import_template")


@user_router.post("/import")
async def import_user(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import user information from a file.

    Args:
        file: The file containing user information to import.

    Returns:
        Success result message
    """
    success_count = await user_service.import_user(file=file)
    return result.success(data=f"Success import count: {success_count}")


@user_router.get("/users")
async def users(user_filter_form: Annotated[UserFilterForm, Query()]) -> Dict:
    """
    Filter users with pagination.

    Args:
        user_filter_form: Pagination and filter info to query

    Returns:
        UserQuery list and total count.
    """
    records, total_count = await user_service.users(data=user_filter_form)
    return result.success(data={"records": records, "total_count": total_count})


@user_router.get("/export")
async def export(
    data: Annotated[UserFilterForm, Query()],
) -> StreamingResponse:
    """
    Export user information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with user info
    """
    return await user_service.export_user(params=data)


@user_router.put("/modify")
async def modify(
    data: UserUpdateCmd,
) -> Dict:
    """
    Update user information.

    Args:
        data: Command containing updated user info.

    Returns:
        Success result message
    """
    await user_service.modify_by_id(
        record=UserDO(**data.model_dump(exclude_unset=True))
    )
    return result.success()


@user_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: UserBatchUpdate) -> Dict:
    password = data.password
    if password is not None:
        if len(password) < 6 or not re.search(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password
        ):
            raise SystemException(
                ResponseCode.PASSWORD_VALID_ERROR.code,
                ResponseCode.PASSWORD_VALID_ERROR.msg,
            )
        data.password = get_password_hash(password)
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await user_service.batch_modify_by_ids(ids=ids.ids, record=cleaned_data)
    return result.success()


@user_router.delete("/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a user by their ID.

    Args:
        id: User ID to remove.

    Returns:
        Success result message
    """
    await user_service.remove_by_id(id=id)
    return result.success()


@user_router.delete("/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete users by a list of IDs.

    Args:

        ids: List of user IDs to delete.

    Returns:
        Success result message
    """
    await user_service.batch_remove_by_ids(ids=ids)
    return result.success()


@user_router.post("/logout")
async def logout():
    return result.success()


@user_router.get("/menus")
async def menus():
    data = [
        {
            "icon": "system-manage",
            "orderNo": 2,
            "name": "系统管理",
            "hideMenu": False,
            "path": "/system",
            "children": [
                {
                    "key": "user",
                    "name": "用户管理",
                    "hideMenu": False,
                    "path": "/system/user",
                }
            ],
        },
        {
            "icon": "tool",
            "orderNo": 8,
            "name": "工具箱",
            "hideMenu": False,
            "path": "/tool",
            "children": [
                {
                    "key": "code",
                    "icon": "code",
                    "name": "代码生成",
                    "hideMenu": False,
                    "path": "/tool/code",
                }
            ],
        },
        {
            "icon": "monitor",
            "orderNo": 10,
            "name": "系统监控",
            "hideMenu": False,
            "path": "/monitor",
        },
        {
            "icon": "bug",
            "orderNo": 11,
            "name": "异常页面",
            "hideMenu": True,
            "path": "/exception",
            "children": [
                {
                    "key": "page403",
                    "name": "403页面",
                    "hideMenu": False,
                    "path": "/exception/page-403",
                },
                {
                    "key": "page404",
                    "name": "404页面",
                    "hideMenu": False,
                    "path": "/exception/page-404",
                },
                {
                    "key": "page500",
                    "name": "500页面",
                    "hideMenu": False,
                    "path": "/exception/page-500",
                },
            ],
        },
        {
            "icon": "home",
            "affix": True,
            "orderNo": 1,
            "hideChildrenInMenu": True,
            "name": "首页",
            "hideMenu": False,
            "path": "/home",
        },
    ]
    return BaseResponse(data=data)
