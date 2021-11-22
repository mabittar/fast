from asyncio import get_event_loop
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from infrastructure.database import setting_engine
from main import app
from sqlmodel import Session


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
    app.dependency_overrides[setting_engine] = in_memory_db
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
async def async_client() -> Generator:

    app.dependency_overrides[setting_engine] = in_memory_db
    async with AsyncClient(app=app, base_url="http://testserver") as client:

        yield client


@pytest.fixture(scope="module")
def event_loop():

    loop = get_event_loop()

    yield loop
