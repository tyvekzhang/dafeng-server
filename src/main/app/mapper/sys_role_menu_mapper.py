"""RoleMenu mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_role_menu_model import RoleMenuDO


class RoleMenuMapper(SqlModelMapper[RoleMenuDO]):
    pass


roleMenuMapper = RoleMenuMapper(RoleMenuDO)