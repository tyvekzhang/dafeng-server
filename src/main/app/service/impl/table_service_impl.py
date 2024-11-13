"""Table domain service impl"""

from src.main.app.mapper.table_mapper import TableMapper
from src.main.app.model.table_model import TableDO
from src.main.app.service.table_service import TableService
from src.main.app.service.impl.service_base_impl import ServiceBaseImpl


class TableServiceImpl(ServiceBaseImpl[TableMapper, TableDO], TableService):
    """
    Implementation of the TableService interface.
    """

    def __init__(self, mapper: TableMapper):
        """
        Initialize the TableServiceImpl instance.

        Args:
            mapper (TableMapper): The TableMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper
