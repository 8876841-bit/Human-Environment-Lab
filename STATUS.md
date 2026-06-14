# STATUS（仓库状态地图）

> 本文件用于标记仓库内各模块的当前状态，避免把历史方案、实验项目、长期规划误认为当前主线。

---

## 状态标签说明

| 标签 | 含义 |
|---|---|
| `CORE` | 当前主线，优先维护与执行 |
| `FOUNDATION` | 根基层，提供底层理论与模型 |
| `LEGACY` | 历史方案，仅作参考，不作为当前执行依据 |
| `EXPERIMENT` | 实验项目，可用于验证，不作为正式生产底座 |
| `PLANNING` | 规划中，暂缓执行 |
| `SUPPORT` | 支撑文件，用于交接、说明、展示 |

---

## 当前状态总表

| 路径 | 状态 | 说明 |
|---|---|---|
| `README.md` | `SUPPORT` | 项目总入口，需指向当前主线 |
| `CURRENT-MAINLINE.md` | `CORE` | 当前执行主线声明文件 |
| `STATUS.md` | `CORE` | 仓库模块状态地图 |
| `01-观察框架/` | `FOUNDATION` | HEL 底层观察模型，定义总母线、八条母线与核心公式 |
| `02-内容引擎/` | `FOUNDATION` | 早期内容流水线设计，作为 V1 引擎参考 |
| `03-观察日志/` | `CORE` | 真实观察与评论痛点入库位置，当前最需要补强 |
| `04-账号矩阵/` | `LEGACY / LONG-TERM` | 中长期账号矩阵设想，当前阶段不铺 8 个账号 |
| `05-内容生产体系/` | `CORE` | 当前内容体系主线，含转译、视觉、视频、人机协作与 Dify 指南 |
| `06-Dify多Agent工作流/` | `CORE / NEEDS_TEST` | Dify DSL 与知识库搭建资产，需实测联调 |
| `04-外部输入模块/` | `PLANNING` | n8n 多平台采集，二期模块，当前暂缓 |
| `guide/` | `LEGACY` | 早期 Coze/Liblib/TapNow 指南，历史参考 |
| `agent-studio/` | `EXPERIMENT` | 浏览器端工作台，本地实验，不建议公开部署 |
| `hel-agent-workbench/` | `EXPERIMENT` | Python Agent 原型，可用于代码化验证 |
| `index.html` | `SUPPORT` | GitHub Pages 展示页 |
| `HANDOFF.md` | `SUPPORT` | 跨会话交接说明，需要保持最新 |
| `HISTORY.md` | `SUPPORT` | 历史演变记录 |
| `ARCHITECTURE.md` | `SUPPORT` | 架构说明 |
| `DERIVATION.md` | `SUPPORT` | 设计推导与决策依据 |

---

## 当前优先级

### P0：立即执行

```text
03-观察日志/
05-内容生产体系/10-Dify工作流搭建实施指南.md
05-内容生产体系/PROGRESS-会话进展与决策记录.md
```

目标：用真实 OBS 跑通内容生产闭环。

### P1：同步维护

```text
README.md
CURRENT-MAINLINE.md
STATUS.md
HANDOFF.md
```

目标：保证任何新会话、新工具、新协作者打开仓库后不会走错主线。

### P2：实验保留

```text
agent-studio/
hel-agent-workbench/
06-Dify多Agent工作流/
```

目标：保留工具化探索，但不让实验路线压过当前主线。

### P3：暂缓

```text
04-外部输入模块/
04-账号矩阵/
guide/
```

目标：暂不删除，先降级，避免分散注意力。

---

## 当前阶段验收标准

```text
1. 至少 10 条真实 OBS 入库。
2. 至少 3 条内容完成发布。
3. 每条发布内容都有数据复盘。
4. 复盘能反向生成下一轮 OBS。
5. Dify 节点 1 + 节点 2 能稳定跑通。
```
