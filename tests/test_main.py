from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"project": "LuxRestore-AI", "version": "0.1.0"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_locate_debug_endpoint_default():
    payload = {
        "data": "mock_image_path.png",
        "is_path": True
    }
    response = client.post("/locate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "regions" in data
    assert len(data["regions"]) > 0
    assert data["regions"][0]["label"] == "WATERMARK"

def test_locate_debug_endpoint_override():
    payload = {
        "data": "mock_image_path.png",
        "is_path": True
    }
    response = client.post("/locate?provider=FLORENCE2", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "regions" in data
    assert len(data["regions"]) > 0
    assert data["regions"][0]["metadata"].get("florence2_mock") is True
