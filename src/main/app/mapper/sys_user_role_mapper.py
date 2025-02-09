"""UserRole mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_user_role_model import UserRoleDO


class UserRoleMapper(SqlModelMapper[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)