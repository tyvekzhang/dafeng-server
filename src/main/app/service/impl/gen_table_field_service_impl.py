"""GenTableField domain service impl"""
from src.main.app.mapper.gen_field_mapper import GenFieldMapper
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.service.gen_table_field_service import GenTableFieldService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class GenTableFieldServiceImpl(ServiceBaseImpl[GenFieldMapper, GenFieldDO], GenTableFieldService):
    def __init__(self, mapper: GenFieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper