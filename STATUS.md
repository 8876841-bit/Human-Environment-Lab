# STATUS（仓库状态地图）

> 本文件用于标记仓库内各模块的当前状态，避免把历史方案、实验项目、长期规划误认为当前主线。

---

## 当前版本

```text
V3.0：碳基—硅基双分身 Human-Environment-Lab 内核升级阶段
```

当前最高主线：

```text
00-系统内核/
```

当前执行入口：

```text
RUNBOOK.md
```

---

## 状态标签说明

| 标签 | 含义 |
|---|---|
| `CORE` | 当前主线，优先维护与执行 |
| `KERNEL` | V3 顶层系统内核，优先级高于所有执行模块 |
| `FOUNDATION` | 根基层，提供底层理论与历史模型 |
| `OUTPUT` | 表达、传播、内容、平台发布相关模块 |
| `IMPLEMENTATION` | 技术实现层，承接系统执行 |
| `SYNCED` | 已完成当前阶段的 V3 同步 |
| `PARTIAL_SYNC` | 已完成关键入口同步，但仍有子文件需要继续同步 |
| `NEEDS_SYNC` | 内容或 DSL 需要同步 V3 主线 |
| `LEGACY` | 历史方案，仅作参考，不作为当前执行依据 |
| `EXPERIMENT` | 实验项目，可用于验证，不作为正式底座 |
| `PLANNING` | 规划中，暂缓执行 |
| `SUPPORT` | 支撑文件，用于交接、说明、展示 |

---

## 当前状态总表

| 路径 | 状态 | 说明 |
|---|---|---|
| `README.md` | `CORE` | 项目总入口，已升级为 V3 主线入口 |
| `CURRENT-MAINLINE.md` | `CORE` | 当前执行主线声明文件 |
| `STATUS.md` | `CORE` | 仓库模块状态地图 |
| `RUNBOOK.md` | `CORE` | 日常运行手册 |
| `HANDOFF.md` | `CORE` | 跨会话交接说明 |
| `DECISION-LOG.md` | `CORE` | 重大决策记录 |
| `00-系统内核/` | `KERNEL / CORE` | V3 顶层内核：碳基—硅基双分身、Lab 总定义、Loop Engineering 协议 |
| `01-观察框架/` | `FOUNDATION` | HEL 旧底层观察模型，保留为理论根基 |
| `02-内容引擎/` | `FOUNDATION / LEGACY` | 早期内容流水线 V1，保留为历史参考 |
| `03-观察日志/` | `CORE` | 真实触发、观察、反馈和可复用 OBS 的沉淀位置 |
| `04-账号矩阵/` | `LEGACY / LONG-TERM` | 中长期账号矩阵设想，当前阶段不铺 8 个账号 |
| `05-内容生产体系/` | `OUTPUT / PARTIAL_SYNC` | 已改为表达与传播模块；README、硬校验清单、V3 Dify 指南已同步，其他 V2 资产保留为工具库 |
| `06-Dify多Agent工作流/` | `IMPLEMENTATION / PARTIAL_SYNC` | README、总控 Agent、Lab 交付判断 Agent 已同步；脚本、视觉、视频、复盘 Agent 和知识库仍需继续同步 |
| `04-外部输入模块/` | `PLANNING` | n8n 多平台采集，二期模块，当前暂缓 |
| `guide/` | `LEGACY` | 早期 Coze/Liblib/TapNow 指南，历史参考 |
| `agent-studio/` | `EXPERIMENT` | 浏览器端工作台，本地实验，不建议公开部署 |
| `hel-agent-workbench/` | `EXPERIMENT` | Python Agent 原型，可用于代码化验证 |
| `index.html` | `SUPPORT` | GitHub Pages 展示页 |
| `HISTORY.md` | `SUPPORT` | 历史演变记录 |
| `ARCHITECTURE.md` | `SUPPORT` | 架构说明 |
| `DERIVATION.md` | `SUPPORT` | 设计推导与决策依据 |

---

## 当前优先级

### P0：立即执行

```text
00-系统内核/
CURRENT-MAINLINE.md
RUNBOOK.md
03-观察日志/
```

目标：跑通 V3 最小循环。

```text
碳基真实输入
→ 硅基数字处理
→ Lab 交付判断
→ 物理世界验证
→ 数字生命与 Lab 双重迭代
```

---

### P1：同步维护

```text
README.md
STATUS.md
HANDOFF.md
DECISION-LOG.md
ARCHITECTURE.md
```

目标：保证新会话、新工具、新协作者打开仓库后不会误把 V2 内容生产体系当成最高主线。

---

### P2：表达与传播模块同步

```text
05-内容生产体系/
06-Dify多Agent工作流/
```

当前已完成：

```text
05-内容生产体系/README.md
05-内容生产体系/00-内容生产硬校验清单.md
05-内容生产体系/10-Dify工作流搭建实施指南-V3.md
06-Dify多Agent工作流/README.md
06-Dify多Agent工作流/dsl/06-HEL-总控Agent.yml
06-Dify多Agent工作流/dsl/01-HEL-选题Agent.yml
```

下一步继续同步：

```text
06-Dify多Agent工作流/dsl/02-HEL-脚本Agent.yml
06-Dify多Agent工作流/dsl/03-HEL-视觉Agent.yml
06-Dify多Agent工作流/dsl/04-HEL-视频Agent.yml
06-Dify多Agent工作流/dsl/05-HEL-复盘Agent.yml
06-Dify多Agent工作流/knowledge_docs/
```

同步方向：

```text
从：触发点 → 选题 → 脚本 → 发布 → 复盘

升级为：
触发点 → 硅基处理 → Lab 交付判断 → 表达传播执行包 → 现实反馈
```

---

### P3：实验保留

```text
agent-studio/
hel-agent-workbench/
```

目标：保留工具化探索，但不让实验路线压过当前主线。

---

### P4：暂缓

```text
04-外部输入模块/
04-账号矩阵/
guide/
```

目标：暂不删除，先降级，避免分散注意力。

---

## 当前阶段验收标准

```text
1. 至少整理 10 条已有真实触发点。
2. 至少 3 条真实触发点完成 V3 Lab 运行日志。
3. 每条运行日志都包含：碳基输入、硅基处理、Lab 交付判断、证据强度、下一步现实动作。
4. 至少 1 条触发点带回物理世界验证。
5. 至少 1 条反馈写回规则库、OBS 或运行日志。
6. 05-内容生产体系 不再作为最高主线，只作为表达与传播模块调用。
7. Dify 总控入口不再默认进入内容生产，而先进行碳基输入确认与 Lab 交付判断。
```

---

## 当前硬边界

```text
没有真实触发，不进入系统。
没有证据，不写成事实。
没有现实反馈，不进入稳定规则库。
不默认所有触发点都要做成内容。
不把数字生命当普通文案助手。
不把 Human-Environment-Lab 简化成内容工厂。
不把 Dify 总控 Agent 当爆款内容入口。
```

---

*最后更新：2026-06-16*
