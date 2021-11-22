import os

from env_config import settings
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine

sql_file = f"{settings.path}/{str(settings.DB_FILE)}"

connect_args = {"check_same_thread": False}
sqlite_url = f"sqlite:///{sql_file}"


def setting_engine():
    return create_engine(sqlite_url, echo=settings.DB_ECHO, connect_args=connect_args)


def create_db_and_tables():
    database_exists = os.path.exists("sql_file")
    if not database_exists:
        SQLModel.metadata.create_all(setting_engine())


def get_session():
    db = Session(setting_engine())
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
