import time
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.core.config import settings
from app.core.security import SecurityService
from app.rag.vector_store import VectorIndex
from app.agents.react_agent import ReActAgent

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise AI & RAG Microservice com Vector Store em memória e Agente ReAct."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado Global de RAG e Agentes
vector_store = VectorIndex(dimension=settings.EMBEDDING_DIM)
agent = ReActAgent(vector_index=vector_store)

# Modelos Pydantic v2
class IngestionRequest(BaseModel):
    doc_id: str = Field(..., min_length=2)
    chunk_id: str = Field(..., min_length=2)
    text: str = Field(..., min_length=5)
    metadata: Optional[Dict[str, Any]] = None

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=3, ge=1, le=10)

class AgentRunRequest(BaseModel):
    objective: str = Field(..., min_length=3)

# Middleware de Latência e Métricas
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# Rotas do Sistema
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "stack": "python-ai-saas",
        "docs_indexed": vector_store.count(),
        "version": settings.VERSION
    }

@app.get("/metrics")
def prometheus_metrics():
    return {
        "vector_docs_total": vector_store.count(),
        "agent_tools_count": len(agent.tools.get_descriptions()),
        "status": "online"
    }

@app.post("/api/v1/auth/token")
def generate_token(tenant_id: str = "tenant_ai_default", role: str = "member"):
    token = SecurityService.create_api_token(tenant_id, role)
    return {"token": token, "tenant_id": tenant_id, "role": role}

@app.post("/api/v1/rag/ingest")
def ingest_document(req: IngestionRequest):
    chunk = vector_store.insert(
        doc_id=req.doc_id,
        chunk_id=req.chunk_id,
        text=req.text,
        metadata=req.metadata
    )
    return {
        "status": "ingested",
        "doc_id": chunk.doc_id,
        "chunk_id": chunk.chunk_id,
        "total_indexed": vector_store.count()
    }

@app.post("/api/v1/rag/search")
def search_rag(req: SearchRequest):
    hits = vector_store.search(query=req.query, top_k=req.top_k)
    return {"query": req.query, "hits": hits, "count": len(hits)}

@app.post("/api/v1/agent/run")
def execute_agent(req: AgentRunRequest):
    result = agent.run(req.objective)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
