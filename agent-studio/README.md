# agent-studio 目录说明

> 状态：`EXPERIMENT`（实验项目）

`agent-studio/` 是早期浏览器端多 Agent 内容工作台实验。

它用于验证：

```text
选题 Agent
脚本 Agent
画面 Agent
生成 Agent
浏览器端交互界面
```

---

## 当前定位

```text
本地实验可以保留。
不建议作为正式生产主线。
不建议直接公网部署。
```

原因：

- 浏览器端保存 API Key 存在安全风险。
- 前端直接请求模型 API，不适合公开环境。
- 当前仓库主线已经转向 Dify 工作流。

---

## 当前执行主线

请以以下文件为准：

```text
CURRENT-MAINLINE.md
05-内容生产体系/10-Dify工作流搭建实施指南.md
RUNBOOK.md
```

---

## 后续可能用途

```text
1. 做本地交互原型。
2. 验证 UI/UX。
3. 作为未来后端化系统的前端参考。
```

如果未来要正式上线，应改为：

```text
前端界面 → 后端服务 → 模型 API
```

不要让前端直接持有和调用真实 API Key。
