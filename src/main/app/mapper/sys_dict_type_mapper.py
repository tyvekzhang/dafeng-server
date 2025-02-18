"""DictType mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_dict_type_model import DictTypeDO


class DictTypeMapper(SqlModelMapper[DictTypeDO]):
    pass


dictTypeMapper = DictTypeMapper(DictTypeDO)