# model/model_utils.py
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib, os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'if_model.joblib')
def train_model(X):
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def score_model(model, X):
    # anomaly score: -1 means anomaly
    raw = model.predict(X)
    scores = model.decision_function(X)
    return raw, scores
