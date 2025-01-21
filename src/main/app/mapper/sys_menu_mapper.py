"""Menu mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_menu_model import MenuDO


class MenuMapper(SqlModelMapper[MenuDO]):
    pass


menuMapper = MenuMapper(MenuDO)