"""
RAG 索引构建器
扫描仓库 CORE 文件 + 03-观察日志，构建 ChromaDB 向量索引。
每次仓库内容更新后运行: python3 RAG/index_builder.py --force
"""

import os
import sys
import re
import hashlib
from pathlib import Path
from datetime import datetime

import chromadb
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent

# 索引范围
TARGET_DIRS = [
    "00-系统内核",
    "01-观察框架",
    "02-内容引擎",
    "03-观察日志",
    "09-内容与视频执行中台",
    "待整理区",
]

ROOT_FILES = [
    "HANDOFF.md",
    "CURRENT-MAINLINE.md",
    "STATUS.md",
    "ARCHITECTURE.md",
    "STATUS-MANIFEST.md",
    "DECISION-LOG-V3.3.md",
    "RUNBOOK.md",
]

EXCLUDE_STATUS = ["LEGACY", "PENDING", "ASSET", "RESERVED"]
CHROMA_PATH = str(REPO_ROOT / "RAG" / "chroma_db")


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


def is_core_file(filepath: str) -> bool:
    """判断文件状态，排除 LEGACY/PENDING/ASSET"""
    try:
        with open(filepath, "r") as f:
            content = f.read(2048)
        for line in content.split("\n")[:20]:
            if line.startswith("状态：") or line.startswith("状态:"):
                status = line.split("：")[-1].split(":")[-1].strip()
                if status in EXCLUDE_STATUS:
                    return False
                return True
        return True
    except Exception:
        return False


def chunk_markdown(text: str, file_path: str) -> list[dict]:
    """
    按 ## 标题切分文档，保留有意义的段落块。
    返回 [{text, metadata}, ...]
    """
    chunks = []
    sections = re.split(r'\n(?=## )', text)

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) < 80:
            # 短段落和相邻段落合并（由上层逻辑处理）
            # 这里先跳过过短的，避免噪音
            if len(section) < 40:
                continue

        # 提取标题
        title_match = re.match(r'^#{1,3}\s+(.+)', section)
        section_title = title_match.group(1).strip() if title_match else ""

        # 生成唯一 ID
        chunk_id = hashlib.md5(
            f"{file_path}::{section_title}::{section[:100]}".encode()
        ).hexdigest()[:16]

        chunks.append({
            "id": chunk_id,
            "text": section,
            "metadata": {
                "file_path": file_path,
                "section_title": section_title,
            },
        })

    return chunks


def load_documents() -> list[dict]:
    """扫描并加载所有应索引的文件，返回 chunk 列表"""
    all_chunks = []

    def process_file(file_path: Path, rel_path: str):
        if not is_core_file(str(file_path)):
            print(f"  [SKIP] {rel_path}")
            return
        try:
            with open(file_path, "r") as f:
                content = f.read()
            if len(content.strip()) < 50:
                return
            chunks = chunk_markdown(content, rel_path)
            all_chunks.extend(chunks)
            print(f"  [OK] {rel_path} → {len(chunks)} chunks")
        except Exception as e:
            print(f"  [ERROR] {rel_path}: {e}")

    # 目录下的 .md 文件
    for dir_name in TARGET_DIRS:
        dir_path = REPO_ROOT / dir_name
        if not dir_path.exists():
            continue
        for md_file in sorted(dir_path.rglob("*.md")):
            process_file(md_file, str(md_file.relative_to(REPO_ROOT)))

    # 根目录文件
    for file_name in ROOT_FILES:
        file_path = REPO_ROOT / file_name
        if file_path.exists():
            process_file(file_path, file_name)

    return all_chunks


MAX_CHARS = 6000  # embedding 安全长度（8192 tokens ≈ 约 6000 中文字符）


def build_index(force: bool = False):
    print("=" * 60)
    print(f"HEL RAG 索引构建 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in .env")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # 1. 加载文档
    print("\n[1/3] 扫描仓库文件...")
    chunks = load_documents()
    print(f"  -> 共 {len(chunks)} 个块")

    if not chunks:
        print("[ERROR] 没有找到可索引的文档")
        sys.exit(1)

    # 2. 初始化 ChromaDB
    print("\n[2/3] 初始化 ChromaDB...")
    if force:
        import shutil
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print("  -> 已清除旧索引")

    db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection_name = "hel_core"

    try:
        if force:
            db.delete_collection(collection_name)
    except Exception:
        pass

    collection = db.get_or_create_collection(
        name=collection_name,
        metadata={"description": "HEL 仓库核心知识库"},
    )

    # 3. 批量生成嵌入并写入
    print("\n[3/3] 生成嵌入并写入 ChromaDB...")
    batch_size = 20
    total = len(chunks)

    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        # 截断过长文本
        batch_texts = [(c["text"][:MAX_CHARS] if len(c["text"]) > MAX_CHARS else c["text"]) for c in batch]
        batch_ids = [c["id"] for c in batch]
        batch_metadatas = [c["metadata"] for c in batch]

        try:
            resp = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch_texts,
            )
            batch_embeddings = [d.embedding for d in resp.data]
        except Exception as e:
            print(f"  [WARN] batch {i} 出错: {e}, 逐条重试...")
            batch_embeddings = []
            for text in batch_texts:
                try:
                    r = client.embeddings.create(model="text-embedding-3-small", input=text[:6000])
                    batch_embeddings.append(r.data[0].embedding)
                except Exception as e2:
                    print(f"    [SKIP] 单条也失败: {e2}")
                    batch_embeddings.append([0.0] * 1536)  # fallback

        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            documents=[t[:2000] for t in batch_texts],
            metadatas=batch_metadatas,
        )
        print(f"  -> {min(i + batch_size, total)}/{total}")

    print(f"\n✅ 索引构建完成！")
    print(f"   块数: {len(chunks)}")
    print(f"   Collection: {collection_name}")
    print(f"   存储: {CHROMA_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="强制重建索引")
    args = parser.parse_args()
    build_index(force=args.force)
