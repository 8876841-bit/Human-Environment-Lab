# ROUTER · 任务路由规则

> Claude 读取 INBOX 后，按本规则判断任务交给谁。

## 路由表

| 任务类型 | 路由至 | 输出格式 |
|---------|--------|---------|
| 方向判断 / 内容提炼 / 模型纠偏 | ChatGPT | 写入 RESULTS.md |
| 仓库整理 / 文件归档 / 状态维护 | Claude（MimoCode/Claude Code） | 直接执行 |
| 工程脚本 / 自动化 / 网站 / RAG工具 / OSS / API调用 | Codex | 写入 CODEX-TASKS.md |
| 仓库依据检索 / 文件摘要 | RAG（http://127.0.0.1:8765/search） | 检索结果给 Claude |
| 最终是否采纳 / 是否入核心 | 人类倩倩 | 写入 DECISIONS.md |

## 路由原则

1. Claude 不执行工程任务（不做图、不做视频、不写大量代码）→ 交给 Codex
2. Claude 不出最终内容成品（图片）→ 交给 ChatGPT（DALL-E）
3. Codex 不做系统设计判断 → 执行前通过 RAG 查仓库规则
4. RAG 不做判断 → 只返回检索结果
5. 所有 Agent 产出默认写入对应的任务池/结果池
6. 人类倩倩确认后，Claude 搬进 CORE 目录
