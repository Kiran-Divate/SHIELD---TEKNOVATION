# llm/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os, json
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts):
    return MODEL.encode(texts, convert_to_numpy=True)

def build_index(logs):
    # logs: list of dicts with "message" and "timestamp"
    texts = [l['message'] for l in logs]
    embs = embed_texts(texts)
    index = {'texts': texts, 'embs': embs.tolist(), 'ts': [l['timestamp'] for l in logs]}
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'log_index.json'), 'w') as f:
        json.dump(index, f)
    return index

def query_index(q, topk=3):
    import numpy as np, json
    idxf = os.path.join(os.path.dirname(__file__), '..', 'data', 'log_index.json')
    if not os.path.exists(idxf):
        return []
    idx = json.load(open(idxf))
    embs = np.array(idx['embs'])
    qv = embed_texts([q])[0]
    sims = embs.dot(qv) / (np.linalg.norm(embs, axis=1)* (np.linalg.norm(qv)+1e-9))
    ids = sims.argsort()[-topk:][::-1]
    return [{"msg": idx['texts'][i], "ts": idx['ts'][i], "score": float(sims[i])} for i in ids]
