from typing import List
from fastapi import APIRouter, Request
from starlette.responses import Response

basic = APIRouter()


@basic.get("/ping")
async def pong():
    return {"ping": "pong!"}


@basic.get(
    "/status",
    status_code=200,
    tags=["status"],
    description="Status Check",
)
async def health_check(req: Request):
    return Response(status_code=200)


@basic.get(
    "/status/all_routes",
    tags=["status"],
    description="List all available routes"
)
async def get_all_routes(req: Request) -> List[str]:
    # Using FastAPI instance
    url_list = [{"path": route.path, "name": route.name}
                for route in req.app.routes]
    return url_list
