# service/remediation_runner.py
import time, json, os

AUDIT = os.path.join(os.path.dirname(__file__), '..', 'data', 'audit.json')

def safe_scale_action(service, new_count):
    # Mock scaling: just write audit; in real-world call AWS ECS with safety checks.
    entry = {"ts": time.time(), "action": "scale", "service": service, "new_count": new_count, "status": "SUCCESS"}
    _append(entry)
    return {"ok": True, "detail": entry}

def safe_restart_action(service):
    entry = {"ts": time.time(), "action": "restart", "service": service, "status": "SUCCESS"}
    _append(entry)
    return {"ok": True, "detail": entry}

def _append(obj):
    data = []
    if os.path.exists(AUDIT):
        try:
            data = json.load(open(AUDIT))
        except Exception:
            data = []
    data.append(obj)
    with open(AUDIT, "w") as f:
        json.dump(data, f, indent=2)
