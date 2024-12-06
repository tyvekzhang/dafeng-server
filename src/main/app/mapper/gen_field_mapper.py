"""GenField mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.gen_field_model import GenFieldDO


class GenFieldMapper(SqlModelMapper[GenFieldDO]):
    pass


genFieldMapper = GenFieldMapper(GenFieldDO)
