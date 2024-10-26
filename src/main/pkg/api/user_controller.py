"""User operation controller"""

from fastapi import APIRouter

from src.main.pkg.mapper.user_mapper import userMapper
from src.main.pkg.schema import result
from src.main.pkg.schema.user_schema import UserCreateCmd
from src.main.pkg.service.impl.user_service_impl import UserServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO

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
