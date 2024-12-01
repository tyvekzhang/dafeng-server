"""GenTableColumn mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.gen_table_field_model import GenTableColumnDO


class GenTableColumnMapper(SqlModelMapper[GenTableColumnDO]):
    pass


genTableColumnMapper = GenTableColumnMapper(GenTableColumnDO)
