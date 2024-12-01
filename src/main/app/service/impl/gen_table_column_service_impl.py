"""GenTableColumn domain service impl"""
from src.main.app.mapper.gen_table_column_mapper import GenTableColumnMapper
from src.main.app.model.gen_table_field_model import GenTableColumnDO
from src.main.app.service.gen_table_column_service import GenTableColumnService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class GenTableColumnServiceImpl(ServiceBaseImpl[GenTableColumnMapper, GenTableColumnDO], GenTableColumnService):
    def __init__(self, mapper: GenTableColumnMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper