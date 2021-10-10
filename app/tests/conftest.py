from sqlmodel import Session
import os
from pathlib import Path
import sys
import pytest
from os import path, pardir
from dotenv import load_dotenv
from fastapi.testclient import TestClient


@pytest.mark.asyncio
@pytest.fixture
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
    from main import app
    client = TestClient(app)
    yield client
