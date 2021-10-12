from tests.helpers.payloads import new_report_payload


def test_post_report(client):
    response = client.post("/api/reports", json=new_report_payload)
    assert response.status_code == 200
