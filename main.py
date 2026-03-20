from fastapi import FastAPI, Request
from query import rag_query
from parsing import parse_metadata
import json

app = FastAPI()


@app.get("/")
async def root(request: Request):
    # Extract all query params into a dict except for one
    query = request.query_params.get("q")
    relevance_limit = float(request.query_params.get("relevance_limit", 0.5))
    metadata_filters = {k: parse_metadata(v) for k, v in request.query_params.items() if k not in ["q", "relevance_limit"]}
    if not query:
        return {"error": "Query parameter 'q' is required"}
    response = rag_query(query, metadata_filters=metadata_filters, relevance_limit=relevance_limit)
    return {"query": query, "relevance_limit": relevance_limit, "metadata_filters": metadata_filters, "response": response}
