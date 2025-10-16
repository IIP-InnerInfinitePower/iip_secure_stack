from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pydantic import ValidationError
from app.config import API_KEY, RATE_PER_MIN, CORS_ORIGINS
from schemas import PlanRequest
import logging, sys

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(jsonlogger.JsonFormatter())
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

if CORS_ORIGINS:
    CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

limiter = Limiter(get_remote_address, app=app, default_limits=[f"{RATE_PER_MIN}/minute"])

REQS = Counter("api_requests_total", "Total API requests", ["route","method","code"])

@app.after_request
def after(resp):
    try:
        REQS.labels(request.path, request.method, resp.status_code).inc()
    except Exception as e:
        app.logger.warning("after_request error", extra={"error": str(e)})
    return resp

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/metrics")
def metrics():
    return app.response_class(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.post("/plan")
@limiter.limit("10/minute")
def plan():
    if API_KEY and request.headers.get("X-API-Key") != API_KEY:
        return jsonify(error="unauthorized"), 401
    data = request.get_json(silent=True) or {}
    try:
        req = PlanRequest(**data)
    except ValidationError as e:
        return jsonify(error="validation", details=e.errors()), 400
    return jsonify(plan={"client_id": req.client_id, "goal": req.goal, "message":"generated"}), 200


