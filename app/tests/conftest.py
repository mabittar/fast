from sqlmodel import Session
import pytest
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
