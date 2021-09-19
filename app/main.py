import sys
from fastapi import FastAPI
from env_config import settings
from utils.logger import Logger
from fast_api_load import FastAPIStarter
from routers import routers_list

version = f"{sys.version_info.major}.{sys.version_info.minor}"


class App:
    async def on_startup(self):
        Logger(class_name=__name__).info(
            msg=f"{settings.PROJECT_NAME} STARTING...Using python version {version} and Uvicorn with Gunicorn"
        )

    async def on_shutdown(self):
        Logger(class_name=__name__).info(
            msg=f"{settings.PROJECT_NAME} STOPING API..."
        )

    # add new endpoints to init routers path
    # add new middlewares to init middlewares path
    def create(self) -> FastAPI:
        api = FastAPIStarter.start_up(
            title="FastAPI Fast Starter Project",
            routers=routers_list,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
        )

        return api


app = App().create()
