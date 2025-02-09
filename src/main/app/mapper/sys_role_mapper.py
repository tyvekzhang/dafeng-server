"""Role mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_role_model import RoleDO


class RoleMapper(SqlModelMapper[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)