import streamlit as st
import requests
import json

st.title("SentinelAI — S.H.I.E.L.D Dashboard")

# Fetch latest metrics and RCA from Flask backend
try:
    resp = requests.get("http://127.0.0.1:8080/predict")  # your backend endpoint
    data = resp.json()
except:
    st.error("Backend not reachable!")
    st.stop()

# Metrics
st.subheader("Live Metrics")
st.metric("Latency (ms)", data.get("latency_now", "N/A"))
st.metric("Error Rate (%)", data.get("err_now", "N/A"))
st.metric("Kafka Lag", data.get("lag_now", "N/A"))

# Incident Risk
st.subheader("Incident Risk Score")
risk = data.get("incident_risk", 0)
st.progress(risk)

# RCA Panel
st.subheader("Root Cause Analysis")
st.json(data.get("llm_analysis", {}))

# Remediation Buttons
st.subheader("Remediation Actions")
if st.button("Approve: Restart Consumer"):
    requests.post("http://127.0.0.1:8080/remediate", json={"action": "restart_consumer"})
    st.success("Restart triggered!")

if st.button("Approve: Scale Consumer"):
    requests.post("http://127.0.0.1:8080/remediate", json={"action": "scale_consumer"})
    st.success("Scale triggered!")
