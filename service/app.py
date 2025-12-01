# service/app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os, json
from llm.llm_rca import generate_rca
from service.remediation_runner import safe_scale_action, safe_restart_action

app = Flask(__name__, template_folder='templates')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def read_scores():
    p = os.path.join(DATA_DIR, 'scores.csv')
    import pandas as pd
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p, index_col=0, parse_dates=True)
    return df

@app.route('/')
def index():
    df = read_scores()
    if df is None:
        return "No scores present. Run simulator + ingest + model first."
    latest = df.iloc[-1].to_dict()
    return render_template('dashboard.html', latest=latest)

@app.route('/analyze', methods=['POST'])
def analyze():
    payload = request.get_json()
    # expected payload: timestamp string or use latest
    df = read_scores()
    ts = payload.get('ts') or df.index[-1].isoformat()
    row = df.loc[ts]
    metrics = {"latency_p95": float(row['latency_now']), "error_rate": float(row['err_now']), "kafka_consumer_lag": int(row['lag_now'])}
    r = generate_rca(metrics, ts)
    # respond with r and require approval to remediate
    return jsonify(r)

@app.route('/remediate', methods=['POST'])
def remediate():
    body = request.get_json()
    action = body.get('action')
    service = body.get('service', 'order-consumer')
    if action == 'scale':
        new_count = int(body.get('new_count', 3))
        res = safe_scale_action(service, new_count)
        return jsonify(res)
    elif action == 'restart':
        res = safe_restart_action(service)
        return jsonify(res)
    else:
        return jsonify({"ok": False, "err": "unknown action"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
