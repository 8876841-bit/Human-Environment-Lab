# AI 调度中枢

版本：V1.0
状态：CORE
创建：2026-06-24

> 最小 AI 调度中枢。ChatGPT、Claude Code/MimoCode、Codex、RAG 通过本目录文件协作。减少人类倩倩手工复制粘贴。

## 文件说明

| 文件 | 用途 | 谁写 | 谁读 |
|------|------|------|------|
| CURRENT-FACTS.md | 当前事实源清单 | Claude | 全部 |
| INBOX.md | 人类倩倩输入池 | 人类倩倩 | Claude/Codex |
| ROUTER.md | 任务路由规则 | Claude | 全部 |
| RAG-CONTEXT.md | RAG检索依据池 | Claude | RAG |
| CHATGPT-BRIEF.md | ChatGPT判断简报 | Claude→ChatGPT | ChatGPT |
| CODEX-TASKS.md | Codex工程任务池 | Claude→Codex | Codex |
| RESULTS.md | 执行结果池 | Codex/ChatGPT | Claude/人类倩倩 |
| DECISIONS.md | 用户裁决记录 | 人类倩倩/Claude | 全部 |
| ACCEPTANCE-CHECKLIST.md | 验收清单 | Claude | Claude/Codex |

## 使用流程

```
人类倩倩输入 → INBOX.md
        ↓
Claude 读取 CURRENT-FACTS + RAG检索
        ↓
Claude 判断任务类型 → ROUTER.md
        ↓
┌─ 方向判断/内容 → CHATGPT-BRIEF.md → ChatGPT执行 → RESULTS.md
├─ 工程/自动化    → CODEX-TASKS.md    → Codex执行   → RESULTS.md
└─ 仓库维护      → Claude执行
        ↓
Claude 读 RESULTS.md，决定是否采纳
        ↓
人类倩倩确认 → DECISIONS.md
        ↓
Claude 更新 HANDOFF / STATUS-MANIFEST
```
