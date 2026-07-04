from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "model_present" in body


def test_attendance_list_empty():
    response = client.get("/attendance/all")
    assert response.status_code == 200
    assert response.json()["records"] == []
