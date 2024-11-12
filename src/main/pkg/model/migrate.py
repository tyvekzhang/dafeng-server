"""Use when performing database migration"""

from src.main.pkg.model.user_model import UserDO  # noqa

from src.main.pkg.model.connection_model import ConnectionDO  # noqa
from src.main.pkg.model.database_model import DatabaseDO  # noqa
from src.main.pkg.model.table_model import TableDO  # noqa
from src.main.pkg.model.field_model import FieldDO  # noqa
from src.main.pkg.model.index_model import IndexDO  # noqa

start_signal = "Welcome! autogenerate is processing!"
