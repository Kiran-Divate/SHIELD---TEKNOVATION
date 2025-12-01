# SentinelAI - Hackathon MVP

## Overview
SentinelAI is an end-to-end demo for **AI-Driven Incident Prediction & Auto-Remediation** aimed at Teknovation 2.0.
This repo contains a local-safe, demo-ready pipeline:
simulator -> ingest -> feature build -> model -> LLM RCA -> decision UI -> remediation runner (mock)

## Quick start (local)
1. Create venv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Generate synthetic events:
   ```bash
   python simulator/generate_events.py
   ```
3. Build features:
   ```bash
   python ingest/preprocessor.py
   ```
4. Train model and generate scores:
   ```bash
   python model/train_predict.py
   ```
5. (Optional) Build a simple log index for RCA. Example: collect messages from `data/event_*.json` into `data/log_index.json`.
6. Start the web service:
   ```bash
   python service/app.py
   ```
7. Open `http://localhost:8080/` and click **Request RCA** → approve remediation.

## Notes
- All remediation actions are **mock/safe** and only write to `data/audit.json`.
- Replace the placeholder LLM in `llm/llm_rca.py` with a real API call if desired.
- If `prophet` or heavy libs cause install issues, remove them from `requirements.txt` and rely on the IsolationForest.
