# Human-Environment-Lab 交接说明

> 本文件用于跨工具、跨会话接续。进入新会话后，先读本文件，再读 `CURRENT-MAINLINE.md`。

---

## 当前任务状态

仓库已进入：

```text
V2.1：仓库治理 + 生产验证阶段
```

当前重点不是继续扩展新模块，而是：

```text
治理主线
↓
补真实 OBS
↓
跑通 Dify 节点 1 + 节点 2
↓
发布内容
↓
记录复盘
```

---

## 当前主线

当前唯一执行主线：

```text
05-内容生产体系/10-Dify工作流搭建实施指南.md
```

当前内容体系入口：

```text
05-内容生产体系/README.md
```

当前治理入口：

```text
CURRENT-MAINLINE.md
STATUS.md
DECISION-LOG.md
RUNBOOK.md
```

---

## 当前已经完成的治理动作

1. 新增 `CURRENT-MAINLINE.md`：声明当前主线。
2. 新增 `STATUS.md`：标记各目录状态。
3. 新增 `DECISION-LOG.md`：记录重大决策。
4. 新增 `RUNBOOK.md`：日常运行手册。
5. 更新 `README.md`：指向当前主线。
6. 给 `guide/` 新增 README，标注为历史方案。
7. 给 `04-账号矩阵/` 新增 README，标注为中长期设想。
8. 给 `agent-studio/` 新增 README，标注为实验项目。
9. 给 `hel-agent-workbench/` 新增 README，标注为实验项目。
10. 明确 OBS 不等于装修案例，八条母线都可以作为真实观察入口。

---

## 当前模块状态

| 模块 | 状态 | 说明 |
|---|---|---|
| `01-观察框架/` | FOUNDATION | 底层理论框架 |
| `02-内容引擎/` | FOUNDATION | 早期内容流水线 V1 |
| `03-观察日志/` | CORE | 当前最需要补强的真实观察库 |
| `05-内容生产体系/` | CORE | 当前内容体系主线 |
| `06-Dify多Agent工作流/` | CORE / NEEDS_TEST | Dify DSL 与知识库资产，需实测联调 |
| `guide/` | LEGACY | 早期 Coze/Liblib/TapNow 指南 |
| `04-账号矩阵/` | LEGACY / LONG-TERM | 中长期设想，当前不铺 8 个账号 |
| `agent-studio/` | EXPERIMENT | 浏览器端实验工作台 |
| `hel-agent-workbench/` | EXPERIMENT | Python Agent 原型 |
| `04-外部输入模块/` | PLANNING | n8n 外部输入，二期再做 |

---

## 当前最重要的下一步

```text
建立 10 条真实 OBS。
```

这 10 条 OBS 不要求来自装修，更推荐覆盖至少 4 条母线。

建议结构：

```text
1. AI 工具越多，反而越不知道怎么开始
2. Codex / Claude Code 改变了“做项目”的方式
3. 工作室停滞后，旧身份开始失效
4. 不想做 AI 时代牛马，真实生活反而更重要
5. 客户缺的不是工厂，而是判断系统
6. 谁设计谁收费，谁管理谁担责
7. 家里越住越乱，不一定是人懒
8. 某种材料 / 灯光 / 颜色为什么让人安心或压抑
9. 一个家的布局暴露了家庭运行方式
10. AI 越强，人为什么还需要真实生活
```

每条 OBS 使用：

```text
03-观察日志/OBS-模板.md
```

---

## 当前不要做的事

```text
不要把 HEL 收窄成装修号。
不要继续扩 8 个账号。
不要继续新增视觉形式。
不要继续堆更多 Agent 名字。
不要急着做 n8n 全平台采集。
不要把 agent-studio 公开部署。
不要把系统包装成已经全自动成片。
```

---

## 新会话第一句话建议

```text
请先阅读 HANDOFF.md、CURRENT-MAINLINE.md、STATUS.md 和 RUNBOOK.md，然后继续推进 03-观察日志 的真实 OBS 入库工作。
```

---

## 当前判断

HEL 当前不是缺框架，而是缺真实运行数据。

下一阶段只看三个指标：

```text
1. 入库了多少条真实 OBS？
2. 发布了多少条内容？
3. 复盘有没有反向生成新的 OBS？
```
