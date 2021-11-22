import asyncio
import socket
from typing import Any
from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from infrastructure.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/health_check", tags=["Health"])


@router.get("/", include_in_schema=False, description="health check ping endpoint", status_code=200)
async def health():
    try:
        return Response(status_code=200)
    except Exception:
        return Response(status_code=503)


@router.get(
    "/health_check/all_routes", include_in_schema=False, description="List all available routes", status_code=200
)
async def get_all_routes(req: Request) -> List[Dict[str, Any]]:
    # Using FastAPI instance
    url_list = [{"path": route.path, "name": route.name} for route in req.app.routes]
    return url_list
