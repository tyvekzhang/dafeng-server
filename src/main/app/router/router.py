"""Routing of system modules"""

from fastapi import APIRouter

from src.main.app.controller.probe_controller import probe_router
from src.main.app.controller.user_controller import user_router
from src.main.app.controller.database_controller import database_router
from src.main.app.controller.connection_controller import connection_router
from src.main.app.controller.table_controller import table_router
from src.main.app.controller.field_controller import field_router
from src.main.app.controller.index_controller import index_router
from src.main.app.controller.gen_table_column_controller import gen_table_column_router
from src.main.app.controller.gen_table_controller import gen_table_router

def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(probe_router, tags=["probe"], prefix="/probe")
    router.include_router(user_router, tags=["user"], prefix="/user")
    router.include_router(database_router, tags=["database"], prefix="/database")
    router.include_router(connection_router, tags=["connection"], prefix="/connection")
    router.include_router(table_router, tags=["table"], prefix="/table")
    router.include_router(field_router, tags=["field"], prefix="/field")
    router.include_router(index_router, tags=["index"], prefix="/index")
    router.include_router(gen_table_router, tags=["genTable"], prefix="/gen-table")
    router.include_router(gen_table_column_router, tags=["genTableColumn"], prefix="/gen-table-column")
    return router
