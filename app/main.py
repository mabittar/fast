import sys
import os.path
from env_config import EnvSettings
from env_config import settings
from fast_api_load import FastAPIStarter
from fastapi import FastAPI
from infrastructure.database import create_db_and_tables
from routers import routers_list
from utils.logger import Logger

version = f"{sys.version_info.major}.{sys.version_info.minor}"


def get_settings():
    return EnvSettings()


class App:
    async def on_startup(self):
        logger = Logger(class_name=__name__)
        logger.info(msg=f"{settings.PROJECT_NAME} STARTING...Using python version {version} and Uvicorn with Gunicorn")
        logger.info(msg="Loading Settings")
        get_settings()
        logger.info(msg="Creating Database")
        create_db_and_tables()

    async def on_shutdown(self):
        Logger(class_name=__name__).info(msg=f"{settings.PROJECT_NAME} STOPING API...")

    # add new endpoints to init routers path
    # add new middlewares to init middlewares path
    def create(self) -> FastAPI:
        api = FastAPIStarter.start_up(
            title=settings.PROJECT_NAME,
            routers=routers_list,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
        )

        return api


app = App().create()
