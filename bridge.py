import os
from flask import Flask, jsonify

API_KEY = os.getenv("API_KEY", "")

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200


@app.get("/")
def root():
    return jsonify(status="ok"), 200
