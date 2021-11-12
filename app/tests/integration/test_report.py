import pytest
from tests.helpers.payloads import new_report_payload


@pytest.mark.asyncio
async def test_path_operation_not_found(async_client):
    response = await async_client.get("/reports")
    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test_get_report(async_client):
    response = await async_client.get("/api/reports")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_paginated_report(async_client):
    len_data = 3
    response = await async_client.get(f"/api/reports?page=0&page_size={len_data}")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len_data


@pytest.mark.asyncio
async def test_post_report(async_client):
    response = await async_client.post("/api/reports", json=new_report_payload)
    assert response.status_code == 201
    data = response.json()
    assert data['description'] == "Teste!"
    assert data['city'] == "Sao Paulo"
