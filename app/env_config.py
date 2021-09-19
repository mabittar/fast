import json
import multiprocessing
import os
from typing import List, Union

from dotenv.main import load_dotenv
from pydantic import BaseSettings, Field, validator
from pydantic.networks import AnyHttpUrl

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
use_max_workers = None
if max_workers_str:
    use_max_workers = int(max_workers_str)
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
errorlog = use_errorlog
worker_tmp_dir = "/dev/shm"
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)

# ENV Settings

class EnvSettings(BaseSettings):
    service_root = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(service_root, os.pardir))
    load_dotenv(dotenv_path="../local.env".format(project_root))
    DB_USERNAME: str = Field(default=None, env="DB_USERNAME")
    DB_PASSWORD: str = Field(default=None, env="DB_PASSWORD")
    DB_HOST: str = Field(default="127.0.0.1", env="DB_HOST")
    DB_PORT: int = Field(default=3360, env="DB_PORT")
    DB_POOL_SIZE: int = Field(default="-1", env="DB_POOL_SIZE")
    PROJECT_NAME: str = Field(default="fastapi_starter", env="PROJECT_NAME")
    url_path = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{PROJECT_NAME}'

    # if the project has db access auth uncomment this line and comment next one
    # DB_URL: str = Field(default=url_path)
    
    DB_URL: str = Field(
        default="sqlite+aiosqlite:///:memory:", env="DATABASE_URL")


    back_end_cors_origins: List[AnyHttpUrl] = []

    @validator("back_end_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = EnvSettings()


# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "host": host,
    "port": port,
}

db_path = f"{settings.DB_HOST}:{settings.DB_PORT}"
project_path = f"project_root"
db_data = dict(
    project_name=settings.PROJECT_NAME,
    project_path=project_path,
    db_url=settings.DB_URL,
    db_path=db_path,
    db_pool_size=settings.DB_POOL_SIZE,
)

print(json.dumps(log_data))
print(json.dumps(db_data))
