"""
FastAPI service: natural language → SPARQL → JSON results.

POST /v1/query
  Input:  {"text": "What is the width of a Yamaha P-150?"}
  Output: {"query": ..., "sparql": ..., "results": [...], "answer": ...}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from react import react

app = FastAPI(title="Text-to-Query", version="1.0.0")


class QueryInput(BaseModel):
    text: str


@app.post("/v1/query")
def query_endpoint(q: QueryInput):
    if not q.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")

    result = react(q.text)

    return {
        "query": q.text,
        "answer": result["answer"],
        "sparql": result["sparql"],
        "results": result["results"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
