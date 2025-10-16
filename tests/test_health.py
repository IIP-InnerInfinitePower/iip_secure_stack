from app.app import app

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.is_json and r.get_json().get("status") == "ok"
