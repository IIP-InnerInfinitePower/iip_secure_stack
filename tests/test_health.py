import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from bridge import app

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.is_json and r.get_json() == {"status": "ok"}
