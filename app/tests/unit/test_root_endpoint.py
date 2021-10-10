


def test_healthcheck_endpoint(client):
    response = client.get("/health_check")
    assert response.status_code == 200
