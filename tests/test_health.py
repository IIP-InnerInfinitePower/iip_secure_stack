from app.app import app


def test_health():
    client = app.test_client()
    r = client.get("/health")
    if r.status_code != 200:
        raise AssertionError("Health endpoint failed")
    if not (r.is_json and r.get_json().get("status") == "ok"):
        raise AssertionError("Invalid health response")
