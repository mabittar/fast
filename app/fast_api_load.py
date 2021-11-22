from os.path import realpath
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence

from env_config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


class FastAPIStarter:
    @classmethod
    def start_up(
        cls,
        title: str = settings.PROJECT_NAME,
        routers: Optional[List] = None,
        middlewares: Optional[List] = None,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
    ) -> FastAPI:

        # edit documentation URI
        swagger_url = f"/docs/"

        api = FastAPI(
            title=title,
            docs_url=swagger_url,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )
        
        api.mount("/static", StaticFiles(directory=realpath(f'{realpath(__file__)}/../static')), name="static")

        if settings.back_end_cors_origins:
            api.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                allow_credentials=True,
            )

        if middlewares:
            for middleware in middlewares[::-1]:
                api.add_middleware(middleware)

        if routers:
            for router in routers[::-1]:
                api.include_router(router)

        return api
