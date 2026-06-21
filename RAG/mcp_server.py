#!/usr/bin/env python3
"""
HEL RAG MCP Server
为 Claude Code 提供仓库知识检索工具。

Claude Code 通过 stdio (JSON-RPC) 与本服务通信，
本服务调用本地 RAG API (127.0.0.1:8765) 完成检索。

配置方式（.claude/settings.local.json）:
{
  "mcpServers": {
    "hel-rag": {
      "command": "python3",
      "args": ["RAG/mcp_server.py"],
      "cwd": "/private/tmp/Human-Environment-Lab"
    }
  }
}
"""

import json
import sys
import urllib.request
import urllib.parse
import os

RAG_API = "http://127.0.0.1:8765"


def log(msg: str):
    """输出到 stderr 以便调试（stdout 用于 MCP 协议通信）"""
    print(f"[MCP] {msg}", file=sys.stderr, flush=True)


def call_rag(query: str, top_k: int = 5) -> dict:
    """调用 RAG 检索 API"""
    params = urllib.parse.urlencode({"q": query, "top_k": top_k})
    url = f"{RAG_API}/search?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e), "results": [], "total": 0}


def format_results(data: dict) -> str:
    """将检索结果格式化为 Claude 可读的文本"""
    if data.get("error"):
        return f"检索出错: {data['error']}"

    results = data.get("results", [])
    if not results:
        return "未找到相关内容。"

    lines = [f"查询「{data.get('query', '')}」找到 {len(results)} 条结果:\n"]
    for i, r in enumerate(results, 1):
        file_path = r.get("file_path", "unknown")
        section = r.get("section_title", "")
        score = r.get("score", 0)
        content = r.get("content", "")[:600]
        header = f"## {section}" if section else ""
        lines.append(
            f"### [{i}] {file_path} （相关度 {score:.2f}）\n"
            f"{header}\n"
            f"{content}\n"
        )
    return "\n".join(lines)


# MCP 协议处理
TOOLS = [
    {
        "name": "search_hel_knowledge",
        "description": (
            "检索 Human-Environment-Lab 仓库的核心知识库。"
            "包含 ROOT-LOCK 根基锁定、观察框架、内容引擎、执行中台、"
            "活人感随想、问题追踪等所有 CORE 文件。"
            "可用于查找方向判断、内容原则、脚本规范、表达标准、"
            "历史讨论结论等任何写入仓库的知识。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "检索查询，用中文描述要查找的内容",
                },
                "top_k": {
                    "type": "integer",
                    "description": "返回结果数量，默认5",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    }
]


def handle_request(req: dict) -> dict:
    """处理单个 JSON-RPC 请求"""
    method = req.get("method", "")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "hel-rag",
                    "version": "1.0.0",
                },
            },
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "search_hel_knowledge":
            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 5)
            data = call_rag(query, top_k)
            result_text = format_results(data)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                },
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
        }

    elif method == "notifications/initialized":
        # 通知不需要响应
        return None

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Unknown method: {method}"},
        }


def main():
    log("HEL RAG MCP Server 启动")
    log(f"RAG API: {RAG_API}")

    # 确保当前目录是仓库根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError as e:
            log(f"JSON 解析错误: {e}")
        except Exception as e:
            log(f"处理错误: {e}")


if __name__ == "__main__":
    main()
