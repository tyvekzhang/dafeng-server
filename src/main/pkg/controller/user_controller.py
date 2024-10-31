"""User operation controller"""

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from jwt import PyJWTError

from src.main.pkg.mapper.user_mapper import userMapper
from src.main.pkg.schema import result
from src.main.pkg.schema.common_schema import Token, CurrentUser
from src.main.pkg.schema.result import BaseResponse
from src.main.pkg.schema.user_schema import (
    UserCreateCmd,
    LoginCmd,
    UserQuery,
    RefreshToken,
)
from src.main.pkg.service.impl.user_service_impl import UserServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO
from src.main.pkg.util.security_util import (
    get_current_user,
    is_token_valid,
    get_user_id,
)

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)


@user_router.post("/register")
async def register_user(
    user_create_cmd: UserCreateCmd,
) -> dict:
    """
    Registers a new user.

    Args:

        user_create_cmd: Data required for registration.

    Returns:
        BaseResponse with new user's ID.
    """
    user: UserDO = await user_service.register(user_create_cmd=user_create_cmd)
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
async def get_user(
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

@user_router.get("/logout")
async def logout():
    return result.success()

@user_router.get("/dynamicMenu")
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
