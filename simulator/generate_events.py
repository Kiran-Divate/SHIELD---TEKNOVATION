# simulator/generate_events.py
import json, time, random, os
from datetime import datetime, timedelta

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)

SERVICE = "order-consumer"
def gen_metric(t, baseline=100):
    # baseline p95 latency in ms
    noise = random.gauss(0, 5)
    return max(10, baseline + noise + (50 if random.random() < 0.0 else 0))

def gen_log(t, severity="INFO", msg="ok"):
    return {
        "timestamp": t.isoformat(),
        "service": SERVICE,
        "severity": severity,
        "message": msg
    }

def write_event(ts, metrics, logs, fname):
    obj = {"timestamp": ts.isoformat(), "metrics": metrics, "logs": logs}
    with open(os.path.join(OUT_DIR, fname), "w") as f:
        json.dump(obj, f)

def simulate(duration_minutes=30, anomaly_at=10):
    now = datetime.utcnow()
    events = []
    for i in range(duration_minutes):
        t = now + timedelta(minutes=i)
        base = 100
        # insert anomaly period
        if anomaly_at <= i < anomaly_at + 6:
            latency = gen_metric(t, baseline=400 + random.gauss(0,20))
            err_rate = random.uniform(3, 8)
            logs = [gen_log(t, "ERROR", "TimeoutException: downstream call timed out"),
                    gen_log(t, "WARN", "Consumer lag high: 48000")]
        else:
            latency = gen_metric(t, baseline=100)
            err_rate = random.uniform(0, 0.5)
            logs = [gen_log(t, "INFO", "Processed batch ok")]
        metrics = {"latency_p95": latency, "error_rate": err_rate, "kafka_consumer_lag": (48000 if anomaly_at <= i < anomaly_at + 6 else random.randint(0,100))}
        write_event(t, metrics, logs, f"event_{i:03}.json")
    print("Events generated to ./data/*.json")

if __name__ == "__main__":
    simulate(30, anomaly_at=10)
