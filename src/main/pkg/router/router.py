"""Routing of system modules"""

from fastapi import APIRouter

from src.main.pkg.controller.probe_controller import probe_router
from src.main.pkg.controller.user_controller import user_router
from src.main.pkg.controller.database_controller import table_router


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(probe_router, tags=["probe"], prefix="/probe")
    router.include_router(user_router, tags=["user"], prefix="/user")
    router.include_router(table_router, tags=["database"], prefix="/database")
    return router
