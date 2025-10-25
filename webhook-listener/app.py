from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os, threading, queue, time, yaml
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

ALERTS_TOTAL = Counter('iip_alerts_total','Total alerts received',['status'])
INTEGRITY    = Gauge('iip_integrity_score','Integrity score')
ACTIONS      = Counter('iip_actions_total','Remediation actions taken',['action','result'])
ACTIVE       = Gauge('iip_remediation_active','Active remediations')
DURATION     = Histogram('iip_remediation_seconds','Remediation duration seconds')

POLICY_PATH = os.environ.get('IIP_POLICY','/app/policies.yml')
POLICY = {'rules':[]}
if os.path.exists(POLICY_PATH):
    with open(POLICY_PATH,'r') as f:
        POLICY = yaml.safe_load(f) or {'rules':[]}

Q = queue.Queue()

def apply_action(act):
    t = act.get('type')
    try:
        if t == 'log':
            msg = act.get('message','no-message')
            with open('/tmp/alert_audit.log','a') as f:
                f.write(f"{datetime.now(timezone.utc).isoformat()} ACTION {msg}\n")
            ACTIONS.labels(action='log', result='ok').inc()
        elif t == 'set_integrity':
            v = float(act.get('value', 0))
            INTEGRITY.set(v)
            ACTIONS.labels(action='set_integrity', result='ok').inc()
        else:
            ACTIONS.labels(action=t or 'unknown', result='skip').inc()
    except Exception:
        ACTIONS.labels(action=t or 'unknown', result='error').inc()

def worker():
    while True:
        job = Q.get()
        if job is None: break
        with DURATION.time():
            ACTIVE.inc()
            try:
                for act in job.get('actions', []):
                    apply_action(act)
                time.sleep(0.5)
            finally:
                ACTIVE.dec()
        Q.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.get("/healthz")
def healthz():
    return jsonify(ok=True)

@app.post("/hooks/grafana")
def hook():
    body = request.get_json(silent=True) or {}
    status = body.get('status','unknown')
    ALERTS_TOTAL.labels(status=status).inc()
    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/alert_audit.log","a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} {body}\n")
    alerts = body.get('alerts') or [{}]
    labels = alerts[0].get('labels', {})
    for rule in POLICY.get('rules', []):
        m = rule.get('match', {})
        if all(labels.get(k)==v for k,v in m.items()):
            acts = rule.get('on_firing' if status=='firing' else 'on_resolved', [])
            Q.put({'actions': acts})
            break
    return jsonify(ok=True)

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
