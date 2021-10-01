import os

from env_config import settings
from sqlmodel import Session, SQLModel, create_engine

sql_file = f"{settings.path}/{str(settings.DB_FILE)}"

connect_args = {"check_same_thread": False}
sqlite_url = f"sqlite:///{sql_file}"
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    db = Session(engine)
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
