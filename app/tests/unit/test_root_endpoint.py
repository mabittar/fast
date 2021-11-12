


def test_healthcheck_endpoint(client):
    response = client.get("/health_check")
    assert response.status_code == 200


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == 'home/index.html'
    assert "request" in response.context
