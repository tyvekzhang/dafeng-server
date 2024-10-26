"""Project health probe"""

from fastapi import APIRouter

from src.main.pkg.schema.result import BaseResponse

probe_router = APIRouter()


@probe_router.get("/liveness")
async def liveness():
    """
    Check the system's live status.

    Returns:
        dict: A status object with a 'code' and a 'msg' indicating liveness.
    """
    return BaseResponse()
