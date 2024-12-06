"""GenTableColumn domain service impl"""
from src.main.app.mapper.gen_field_mapper import GenFieldMapper
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.service.gen_table_column_service import GenTableColumnService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class GenTableColumnServiceImpl(ServiceBaseImpl[GenFieldMapper, GenFieldDO], GenTableColumnService):
    def __init__(self, mapper: GenFieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper