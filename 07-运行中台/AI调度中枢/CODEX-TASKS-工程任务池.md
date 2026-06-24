# CODEX-TASKS · 工程任务池（模板）

> Claude 填写后，Codex 读取并执行。结果写入 RESULTS.md。

---

## 模板

```text
任务名称：

输入文件（仓库内路径）：

输出文件（仓库内路径）：

禁止修改：

验收标准：

测试方式：

commit message：
```

---

## 当前任务

### CODEX-001｜检查 AI 调度中枢路径一致性

**任务目标**：编写最小检查脚本，确认 AI 调度中枢关键文件是否存在，避免后续使用简称路径导致执行错误。

**输入文件**：
- 07-运行中台/AI调度中枢/README.md
- 07-运行中台/AI调度中枢/CURRENT-FACTS-当前事实源.md
- 07-运行中台/AI调度中枢/ROUTER-任务路由规则.md
- RAG/RAG-SCOPE.md

**输出文件**：
- scripts/hel_check_ai_hub.py

**脚本要求**：
1. 检查 AI调度中枢关键文件是否存在
2. 检查 RAG/RAG-SCOPE.md 是否存在
3. 检查是否错误引用了不存在的 CURRENT-FACTS.md、RAG-CONTEXT.md、CODEX-TASKS.md 等简称路径
4. 输出清晰的通过/失败报告
5. 不调用外部 API
6. 不引入复杂依赖

**禁止修改**：
- 00-系统内核/ROOT-LOCK-根基锁定.md
- V0.6.1 主模型正文
- 任何 legacy 文件

**验收标准**：
- 运行 `python scripts/hel_check_ai_hub.py`
- 能显示所有关键文件检查结果
- 如果发现简称路径误用，明确报出所在文件

**测试方式**：
```bash
python3 scripts/hel_check_ai_hub.py
```

**commit message**：
```
feat: 添加 AI 调度中枢路径一致性检查脚本
```
