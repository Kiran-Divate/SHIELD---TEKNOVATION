# model/train_predict.py
import pandas as pd
from .model_utils import train_model, load_model, score_model
import os, numpy as np

DATA_FEAT = os.path.join(os.path.dirname(__file__), '..', 'data', 'features.csv')

def main():
    df = pd.read_csv(DATA_FEAT, index_col=0, parse_dates=True)
    # features to use
    X = df[['latency_now','latency_mean','latency_std','err_now','err_mean','lag_now','lag_mean']].astype(float).fillna(0)
    model = load_model()
    if model is None:
        model = train_model(X)
        print("Model trained.")
    raw, scores = score_model(model, X)
    df['anomaly_raw'] = raw
    df['anomaly_score'] = scores
    df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'scores.csv'))
    # produce flagged timestamps & a simple probability mapping
    df['prob'] = (1 - (scores - scores.min())/(scores.max()-scores.min()+1e-9)) # map to 0..1
    out = df[df['anomaly_raw'] == -1][['anomaly_raw','anomaly_score','prob']]
    print("Anomalies found:\n", out.tail(10))
    print("Scores saved to data/scores.csv")

if __name__ == "__main__":
    main()
