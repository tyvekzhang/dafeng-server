"""Routing of system modules"""

from fastapi import APIRouter

from src.main.app.controller.probe_controller import probe_router
from src.main.app.controller.user_controller import user_router
from src.main.app.controller.database_controller import table_router
from src.main.app.controller.connection_controller import connection_router


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(probe_router, tags=["probe"], prefix="/probe")
    router.include_router(user_router, tags=["user"], prefix="/user")
    router.include_router(table_router, tags=["database"], prefix="/database")
    router.include_router(connection_router, tags=["connection"], prefix="/connection")
    return router
