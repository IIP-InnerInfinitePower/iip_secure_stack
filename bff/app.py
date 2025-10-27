from flask import Flask, request, jsonify
import requests, os, re

APP = Flask(__name__)

WEBHOOK_METRICS = os.environ.get("WEBHOOK_METRICS_URL","http://webhook-listener:5001/metrics")

@APP.get("/v1/health")
def health():
    return jsonify(ok=True)

@APP.get("/v1/integrity")
def integrity():
    try:
        r = requests.get(WEBHOOK_METRICS, timeout=2)
        m = re.search(r"^iip_integrity_score\s+([0-9.]+)$", r.text, re.M)
        val = float(m.group(1)) if m else None
        return jsonify(score=val, source="webhook-listener"), 200
    except Exception as e:
        return jsonify(error=str(e)), 502

@APP.post("/v1/intake")
def intake():
    payload = request.get_json(silent=True) or {}
    # stub: accept and echo
    return jsonify(id="stub-001", data=payload), 201

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
