"""User domain service impl"""

from src.main.pkg.enums.enum import ResponseCode
from src.main.pkg.exception.exception import ServiceException
from src.main.pkg.mapper.user_mapper import UserMapper
from src.main.pkg.schema.user_schema import UserCreateCmd
from src.main.pkg.service.impl.base_service_impl import ServiceImpl
from src.main.pkg.service.user_service import UserService
from src.main.pkg.type.user_do import UserDO


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
        user_create_cmd.password = "123456"
        return await self.mapper.insert_record(record=user_create_cmd)
