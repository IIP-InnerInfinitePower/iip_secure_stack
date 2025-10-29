import os, sys
cat > tests/test_health.py <<'PY'
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bridge import app

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.is_json and r.get_json().get("status") == "ok"
