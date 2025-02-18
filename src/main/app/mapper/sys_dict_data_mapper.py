"""DictData mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.sys_dict_data_model import DictDataDO


class DictDataMapper(SqlModelMapper[DictDataDO]):
    pass


dictDataMapper = DictDataMapper(DictDataDO)