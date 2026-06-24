# ACCEPTANCE-CHECKLIST · 验收清单

> 每次执行后 Claude 必须逐项检查。Codex 执行完自己的任务后也需自检。

## 必检项

- [ ] 是否读取了 CURRENT-FACTS-当前事实源.md
- [ ] 是否修改了 ROOT-LOCK 正文（禁止）
- [ ] 是否修改了 V0.6.1 主模型正文（禁止）
- [ ] 是否误用了 legacy 当当前主线
- [ ] 是否更新了 STATUS-MANIFEST.md
- [ ] 是否更新了 HANDOFF.md
- [ ] 是否生成了执行结果
- [ ] 是否需要用户确认
- [ ] 是否新增了不必要复杂度
- [ ] 是否把待整理区草案直接当成最终规则
- [ ] 执行后是否跑了 RAG reindex（`curl -X POST http://127.0.0.1:8765/reindex`）

## 禁止事项

1. 不修改 ROOT-LOCK 正文
2. 不修改 V0.6.1 主模型正文
3. 不删除旧文件
4. 不自动升级版本
5. 不直接改写世界观
6. 不把待整理区草案当最终结论
7. 不让 Codex 或 RAG 做最终判断
8. 不假设 README.md、CURRENT-MAINLINE.md、STATUS.md 必然存在
