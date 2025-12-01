# llm/llm_rca.py
import os, json
from llm.embeddings import query_index
# Placeholder LLM wrapper. Replace with real API call to OpenAI/Anthropic/etc.
def call_llm_system(prompt):
    # For demo, we produce a deterministic, safe mock of an LLM response based on the prompt
    # In prod, this should call OpenAI/Local LLM with system + user prompts.
    return {
        "one_line_rca": "High downstream latency causing consumer backlog; likely downstream timeout.",
        "supporting_lines": [
            "TimeoutException: downstream call timed out",
            "Consumer lag high: 48000",
            "Processed batch failed: retry limit reached"
        ],
        "remediation": "Scale up the order-consumer replica count by 2 and restart failed consumer group.",
        "command_template": "aws ecs update-service --cluster CLUSTER --service order-consumer --desired-count {new_count}",
        "confidence": 78
    }

def generate_rca(metrics, timestamp):
    # semantic search into logs for timestamp window
    q = f"Anomalous logs near {timestamp} with latency {metrics.get('latency_p95')}"
    top = query_index(q, topk=5)
    embedded_logs = "\n".join([t['msg'] for t in top])
    prompt = f"Metrics: {metrics}\nTop logs:\n{embedded_logs}\nGive one-line RCA, supporting lines, remediation command template and confidence."
    resp = call_llm_system(prompt)
    return resp
