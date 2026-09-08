from app import app

def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert "TaskFlow API" in data["message"]

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"

def test_get_tasks():
    client = app.test_client()
    res = client.get("/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert "tasks" in data
    assert data["count"] >= 1
