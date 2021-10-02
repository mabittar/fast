import asyncio
import socket

from fastapi import APIRouter
from fastapi import Depends
from infrastructure.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

router = APIRouter(prefix="/health_check", tags=["Health"])


@router.get("/", status_code=204)
async def health(session: AsyncSession = Depends(get_session)):
    try:
        return Response(status_code=204)
    except Exception:
        return Response(status_code=503)