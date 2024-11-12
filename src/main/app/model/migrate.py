"""Use when performing database migration"""

from src.main.app.model.user_model import UserDO  # noqa

from src.main.app.model.connection_model import ConnectionDO  # noqa
from src.main.app.model.database_model import DatabaseDO  # noqa
from src.main.app.model.table_model import TableDO  # noqa
from src.main.app.model.field_model import FieldDO  # noqa
from src.main.app.model.index_model import IndexDO  # noqa

start_signal = "Welcome! autogenerate is processing!"
