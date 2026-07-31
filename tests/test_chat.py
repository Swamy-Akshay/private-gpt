from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Private GPT!"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_chat():
    response = client.post(
        "/chat",
        json={
            "message": "Pytest Chat"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["message"] == "Pytest Chat"