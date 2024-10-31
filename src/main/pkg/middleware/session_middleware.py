from src.main.pkg.config.config_manager import get_database_config
from src.main.pkg.server import app
from src.main.pkg.session.db_session_middleware import SQLAlchemyMiddleware

db_config = get_database_config()
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(db_config.url),
    engine_args={
        "echo": db_config.echo_sql,
        "pool_recycle": db_config.pool_recycle,
    },
)