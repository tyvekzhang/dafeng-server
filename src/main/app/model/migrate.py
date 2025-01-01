"""Use when performing database migration"""

from src.main.app.model.user_model import UserDO  # noqa

from src.main.app.model.db_connection_model import ConnectionDO  # noqa
from src.main.app.model.db_database_model import DatabaseDO  # noqa
from src.main.app.model.db_table_model import TableDO  # noqa
from src.main.app.model.db_field_model import FieldDO  # noqa
from src.main.app.model.db_index_model import IndexDO  # noqa

from src.main.app.model.gen_field_model import GenFieldDO # noqa
from src.main.app.model.gen_table_model import GenTableDO # noqa

from src.main.app.model.read_new_word_model import {{ class_name }}DO # noqa

start_signal = "Welcome! autogenerate is processing!"
