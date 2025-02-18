"""User operation controller"""

import re
from typing import Dict, Annotated, List

from fastapi import APIRouter, Depends, Query, UploadFile, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse
from jwt import PyJWTError

from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException
from src.main.app.mapper.sys_menu_mapper import menuMapper
from src.main.app.mapper.user_mapper import userMapper
from src.main.app.common import result
from src.main.app.schema.common_schema import Token, CurrentUser
from src.main.app.common.result import HttpResponse
from src.main.app.schema.sys_menu_schema import MenuQuery
from src.main.app.schema.user_schema import (
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
from src.main.app.service.impl.sys_menu_service_impl import MenuServiceImpl
from src.main.app.service.impl.user_service_impl import UserServiceImpl
from src.main.app.service.sys_menu_service import MenuService
from src.main.app.service.user_service import UserService
from src.main.app.model.user_model import UserDO
from src.main.app.common.util.excel_util import export_excel
from src.main.app.common.util.security_util import (
    get_current_user,
    is_token_valid,
    get_user_id,
    get_password_hash,
)

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)


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
) -> HttpResponse[UserQuery]:
    """
    Retrieves the profile of the current user.

    Args:
        current_user: Currently authenticated user.

    Returns:
        BaseResponse with current user's profile information.
    """
    user: UserQuery = await user_service.find_by_id(id=current_user.id)
    return HttpResponse(data=user)


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
    await user_service.modify_by_id(record=UserDO(**data.model_dump(exclude_unset=True)))
    return result.success()


@user_router.put("/batchmodify")
async def batch_modify(ids: Ids, data: UserBatchUpdate) -> Dict:
    password = data.password
    if password is not None:
        if len(password) < 6 or not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password):
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
async def get_menus(request: Request):
    response = await menu_service.fetch_menu_by_page(menu_query=MenuQuery(current=1, pageSize=9999), request=request)
    return HttpResponse(data=response.records)
