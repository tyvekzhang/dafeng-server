"""GlobalWord mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.read_global_word_model import GlobalWordDO


class GlobalWordMapper(SqlModelMapper[GlobalWordDO]):
    pass


globalWordMapper = GlobalWordMapper(GlobalWordDO)