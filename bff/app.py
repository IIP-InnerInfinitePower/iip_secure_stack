from flask import Flask, request, jsonify
import requests, time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQS = Counter("api_requests_total", "Total API requests", ["route","method","code"])
LAT  = Histogram("api_latency_seconds", "Request latency", ["route","method","code"])

def observe(route, method, code, start):
    REQS.labels(route, method, str(code)).inc()
    LAT.labels(route, method, str(code)).observe(time.time()-start)

@app.get("/v1/health")
def health():
    t=time.time()
    resp = jsonify(ok=True); code=200
    observe("/v1/health","GET",code,t); return resp, code

@app.get("/v1/integrity")
def integrity():
    t=time.time()
    try:
        m = requests.get("http://webhook-listener:5001/metrics", timeout=2).text
        score = 0.0
        for line in m.splitlines():
            if line.startswith("iip_integrity_score "):
                score = float(line.split()[1]); break
        resp = jsonify(score=score, source="webhook-listener"); code=200
    except Exception as e:
        resp = jsonify(error=str(e)); code=502
    observe("/v1/integrity","GET",code,t); return resp, code

@app.post("/v1/intake")
def intake():
    t=time.time()
    resp = jsonify(id="stub-001", data=request.get_json(silent=True)); code=201
    observe("/v1/intake","POST",code,t); return resp, code

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
