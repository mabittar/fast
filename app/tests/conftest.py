from typing import Generator
from sqlmodel import Session
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from asyncio import get_event_loop
from main import app

@pytest.fixture(autouse=True)
async def in_memory_db():
    from sqlmodel import create_engine
    engine = create_engine("sqlite:///:memory:")

    return engine


@pytest.mark.asyncio
@pytest.fixture
async def session(engine):
    db = Session(engine)
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()

@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
async def async_client() -> Generator:

    async with AsyncClient(app=app, base_url="http://testserver") as client:

        yield client


@pytest.fixture(scope="module")
def event_loop():

    loop = get_event_loop()

    yield loop
