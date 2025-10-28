import os, json, requests, duckdb, psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
PG_CONN = dict(host=os.getenv("PG_HOST","127.0.0.1"),
               port=int(os.getenv("PG_PORT","5432")),
               dbname=os.getenv("PG_DB","iip_db"),
               user=os.getenv("PG_USER","postgres"),
               password=os.getenv("PG_PASS","postgres"))
DUCK_PATH = os.getenv("DUCK_PATH", os.path.expanduser("~/IIP_SECURE_STACK/data/iip.duckdb"))
LLM_BASE  = os.getenv("LLM_BASE","http://127.0.0.1:8000/v1")
LLM_MODEL = os.getenv("LLM_MODEL")

app = Flask(__name__)

def q_postgres(sql):
    with psycopg2.connect(**PG_CONN) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [c.name for c in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

def q_duckdb(sql):
    con = duckdb.connect(DUCK_PATH)
    try:
        df = con.execute(sql).df()
        return df.to_dict(orient="records")
    finally:
        con.close()

def llm_complete(prompt):
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "max_tokens": 128,
        "temperature": 0.1,
        "stop": ["\n\n", "A:", "```"]
    }
    r = requests.post(f"{LLM_BASE}/completions", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["text"]

@app.post("/ask")
def ask():
    try:
        data = request.get_json(force=True)
        question = (data.get("question") or "").strip()
        source   = (data.get("source") or "pg").strip().lower()  # "pg" or "duck"
        sql      = (data.get("sql") or "").strip()
        if not question or not sql:
            return jsonify(error="Provide 'question' and 'sql'"), 400

        rows = q_postgres(sql) if source == "pg" else q_duckdb(sql)
        sample = rows[:30]
        prompt = (
            "Task: Answer strictly from provided rows.\n"
            "Format: one short sentence. No SQL. No code. No examples. No extra text.\n"
            "If insufficient, reply exactly: insufficient data.\n\n"
            f"Question: {question}\n"
            f"Rows JSON: {json.dumps(sample, ensure_ascii=False)}\n"
            "Answer:"
        )
        answer = llm_complete(prompt).strip()
        return jsonify(answer=answer, rows=len(rows), sample=sample)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
