"""User operation controller"""

from typing import Dict, Annotated, List

from fastapi import APIRouter, Depends, Query, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse
from jwt import PyJWTError

from src.main.pkg.mapper.user_mapper import userMapper
from src.main.pkg.schema import result
from src.main.pkg.schema.common_schema import Token, CurrentUser
from src.main.pkg.schema.result import BaseResponse
from src.main.pkg.schema.user_schema import (
    UserCreate,
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
from src.main.pkg.type.user_do import UserDO
from src.main.pkg.util.excel_util import export_excel
from src.main.pkg.util.security_util import (
    get_current_user,
    is_token_valid,
    get_user_id,
    get_password_hash,
)

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)


@user_router.post("/register")
async def user_register(
    user_create: UserCreate,
) -> Dict:
    """
    Registers a new user.

    Args:
        user_create: Data required for registration.

    Returns:
        BaseResponse with new user's ID.
    """
    user: UserDO = await user_service.register(user_create=user_create)
    return result.success(data=user.id)


@user_router.post("/recover")
async def user_recover(
    user_recover_parm: UserDO,
) -> dict:
    """
    User add .

    Args:
        user_recover_parm: User recover data

    Returns:
        BaseResponse with user's ID.
    """
    user: UserDO = await user_service.save(record=user_recover_parm)
    return result.success(data=user.id)


@user_router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Authenticates user and provides an access token.

    Args:
        login_form: Login credentials.

    Returns:
        Token object with access token.
    """
    login_cmd = LoginCmd(username=login_form.username, password=login_form.password)
    return await user_service.login(login_cmd=login_cmd)


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


@user_router.post("/refreshTokens")
async def refresh_tokens(token: RefreshToken):
    refresh_token = token.refresh_token
    if not is_token_valid(refresh_token):
        raise PyJWTError
    user_id: int = get_user_id(refresh_token)
    return await user_service.generate_tokens(user_id)


@user_router.get("/users")
async def retrieve_user(user_filter_form: Annotated[UserFilterForm, Query()]) -> Dict:
    """
    Filter users with pagination.

    Args:
        user_filter_form: Pagination and filter info to query

    Returns:
        UserQuery list and total count.
    """
    records, total_count = await user_service.retrieve_user(
        user_filter_form=user_filter_form
    )
    return result.success(data={"records": records, "total_count": total_count})


@user_router.put("/update")
async def update_user(
    user_update_cmd: UserUpdateCmd,
) -> Dict:
    """
    Update user information.

    Args:
        user_update_cmd: Command containing updated user info.

    Returns:
        Success result message
    """
    await user_service.modify_by_id(
        record=UserDO(**user_update_cmd.model_dump(exclude_unset=True))
    )
    return result.success()


@user_router.put("/batchUpdate")
async def user_batch_update(
    ids_data: Ids, user_batch_update_data: UserBatchUpdate
) -> Dict:
    if user_batch_update_data.password is not None:
        user_batch_update_data.password = get_password_hash(
            user_batch_update_data.password
        )
    cleaned_data = {
        k: v for k, v in user_batch_update_data.model_dump().items() if v is not None
    }
    if len(cleaned_data) == 0:
        return result.fail("请填写更新的信息")

    await user_service.batch_modify_by_ids(ids=ids_data.ids, record=cleaned_data)
    return result.success()


@user_router.delete("/delete/{id}")
async def delete_user(
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


@user_router.delete("/remove")
async def user_remove_by_ids(
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


@user_router.get("/export")
async def export_user(
    user_filter_form: Annotated[UserFilterForm, Query()],
) -> StreamingResponse:
    """
    Export user information based on provided parameters.

    Args:
        user_filter_form: Filtering and format parameters for export.

    Returns:
        StreamingResponse with user info
    """
    return await user_service.export_user(params=user_filter_form)


@user_router.get("/exportTemplate")
async def export_user_template() -> StreamingResponse:
    """
    Export a template for user information.

    Args:
        current_user: Logged-in user requesting the template.

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

        current_user: Logged-in user performing the import.
    Returns:
        Success result message
    """
    await user_service.import_user(file=file)
    return result.success()


@user_router.get("/logout")
async def logout():
    return result.success()


@user_router.get("/menu")
async def get_menus():
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
