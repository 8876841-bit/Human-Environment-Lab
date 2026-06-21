"""
HEL RAG 检索服务
为 Claude (via MCP) 和 Codex 提供统一的仓库知识检索。

启动: python3 RAG/server.py
默认: http://127.0.0.1:8765
"""

import os
import sys
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import chromadb
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = str(REPO_ROOT / "RAG" / "chroma_db")

app = FastAPI(
    title="HEL RAG Service",
    description="Human-Environment-Lab 仓库知识检索",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_collection = None
_client = None


class SearchResult(BaseModel):
    file_path: str
    section_title: str
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int


class ReindexResponse(BaseModel):
    status: str
    message: str


def load_env():
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    if not os.environ.get(key):
                        os.environ[key] = val


def init():
    global _collection, _client

    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[WARN] OPENAI_API_KEY not set")
        return

    _client = OpenAI(api_key=api_key)

    if not os.path.exists(CHROMA_PATH):
        print("[WARN] 索引不存在，请先运行: python3 RAG/index_builder.py --force")
        return

    try:
        db = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = db.get_collection("hel_core")
        count = _collection.count()
        print(f"[OK] 索引已加载，{count} 条记录")
    except Exception as e:
        print(f"[ERROR] 加载索引失败: {e}")


@app.on_event("startup")
async def startup():
    init()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "collection_loaded": _collection is not None,
        "count": _collection.count() if _collection else 0,
    }


@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="检索查询"),
    top_k: int = Query(5, ge=1, le=20, description="返回结果数"),
):
    """检索仓库知识，返回相关文件片段及其来源"""
    if _collection is None or _client is None:
        return SearchResponse(query=q, results=[], total=0)

    # 生成查询 embedding
    resp = _client.embeddings.create(
        model="text-embedding-3-small",
        input=q,
    )
    query_embedding = resp.data[0].embedding

    # ChromaDB 检索
    chroma_results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    results = []
    if chroma_results["ids"] and chroma_results["ids"][0]:
        for i, doc_id in enumerate(chroma_results["ids"][0]):
            metadata = chroma_results["metadatas"][0][i] if chroma_results["metadatas"][0] else {}
            document = chroma_results["documents"][0][i] if chroma_results["documents"][0] else ""
            distance = chroma_results["distances"][0][i] if chroma_results["distances"][0] else 0

            results.append(SearchResult(
                file_path=metadata.get("file_path", "unknown"),
                section_title=metadata.get("section_title", ""),
                content=document[:800],
                score=round(1.0 / (1.0 + distance), 4),  # distance → similarity
            ))

    return SearchResponse(query=q, results=results, total=len(results))


@app.post("/reindex", response_model=ReindexResponse)
async def reindex():
    """触发索引重建"""
    try:
        import subprocess
        builder = REPO_ROOT / "RAG" / "index_builder.py"
        result = subprocess.run(
            ["python3", str(builder), "--force"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            init()
            return ReindexResponse(status="ok", message="索引重建成功")
        return ReindexResponse(status="error", message=result.stderr[-500:])
    except Exception as e:
        return ReindexResponse(status="error", message=str(e))


if __name__ == "__main__":
    print("=" * 50)
    print("HEL RAG Service")
    print(f"仓库: {REPO_ROOT}")
    print(f"索引: {CHROMA_PATH}")
    print("http://127.0.0.1:8765")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")
