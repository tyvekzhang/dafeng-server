"""User operation controller"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.main.pkg.mapper.user_mapper import userMapper
from src.main.pkg.schema import result
from src.main.pkg.schema.common_schema import Token, CurrentUser
from src.main.pkg.schema.result import BaseResponse
from src.main.pkg.schema.user_schema import UserCreateCmd, LoginCmd, UserQuery
from src.main.pkg.service.impl.user_service_impl import UserServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO
from src.main.pkg.util.security_util import get_current_user

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
) -> BaseResponse[Token]:
    """
    Authenticates user and provides an access token.

    Args:

        login_form: Login credentials.

    Returns:
        Token object with access token.
    """
    login_cmd = LoginCmd(username=login_form.username, password=login_form.password)
    return BaseResponse(data=await user_service.login(login_cmd=login_cmd))


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
