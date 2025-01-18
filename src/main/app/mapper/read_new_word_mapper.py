"""NewWord mapper"""

from src.main.app.mapper.mapper_base_impl import SqlModelMapper
from src.main.app.model.read_new_word_model import NewWordDO


class NewWordMapper(SqlModelMapper[NewWordDO]):
    pass


newWordMapper = NewWordMapper(NewWordDO)