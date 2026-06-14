# hel-agent-workbench 目录说明

> 状态：`EXPERIMENT`（实验项目）

`hel-agent-workbench/` 是 HEL 的 Python 版 Agent 原型，用于验证内容生产流程的代码化能力。

它主要验证：

```text
主题输入
↓
选题 Agent
↓
脚本 Agent
↓
视觉 Agent
↓
生成 Agent
↓
结果保存
```

---

## 当前定位

```text
可以用于本地验证。
不作为当前长期生产主线。
当前长期主线是 Dify 工作流。
```

---

## 已知治理要求

后续如果继续维护，需要优先修正：

```text
1. 不要默认选择第一个选题，应加入人工选择节点。
2. 补充 requirements.txt。
3. 补充 config.example.yaml。
4. 输出 Markdown 内容包，而不只是 JSON。
5. 增强 JSON 解析失败时的错误处理。
6. 图片/视频生成失败时，不应阻断脚本和分镜输出。
```

---

## 当前执行主线

请以以下文件为准：

```text
CURRENT-MAINLINE.md
RUNBOOK.md
05-内容生产体系/10-Dify工作流搭建实施指南.md
```
