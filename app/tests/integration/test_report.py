from main import app
from httpx import AsyncClient
import pytest


payload = {
    "description": "Teste!",
    "city": "Sao Paulo",
    "state": "SP",
    "country": "BR"
}

@pytest.mark.anyio
async def test_post_new_report():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(url="/api/reports", data=payload)
    assert response.status_code == 201
