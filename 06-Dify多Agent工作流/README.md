# HEL Dify 多 Agent 工作流

本目录包含 HEL 内容生产流水线在 Dify 平台的完整搭建资产，包括 6 个 Agent 的 DSL 配置文件和 3 个知识库文档。

## 目录结构

```
06-Dify多Agent工作流/
├── dsl/                          ← 6 个 Agent 的 DSL 配置文件（直接导入 Dify）
│   ├── 01-HEL-选题Agent.yml      ← 📌 选题策划（挂 KB1+KB2）
│   ├── 02-HEL-脚本Agent.yml      ← ✍️ 脚本编导（挂 KB2+KB3）
│   ├── 03-HEL-视觉Agent.yml      ← 🎨 图文美术（挂 KB3）
│   ├── 04-HEL-视频Agent.yml      ← 🎬 视频导演（无需挂库）
│   ├── 05-HEL-复盘Agent.yml      ← 🔍 数据复盘（无需挂库）
│   └── 06-HEL-总控Agent.yml      ← 🧠 总控调度（主入口，无需挂库）
│
└── knowledge_docs/               ← 3 个知识库文档（上传到 Dify Knowledge）
    ├── KB1-底层模型与话题母线.md  ← 知识库1（选题Agent用）
    ├── KB2-概念转译对照表.md      ← 知识库2（选题+脚本Agent用）
    └── KB3-脚本模板与视觉风格.md  ← 知识库3（脚本+视觉Agent用）
```

## 搭建步骤

### 第一步：创建 3 个知识库

进入 [Dify](https://cloud.dify.ai) → **Knowledge** → **Create Knowledge**

依次上传 `knowledge_docs/` 下的 3 个文件，名称如下：

| 文件 | 知识库名称 |
| :--- | :--- |
| KB1-底层模型与话题母线.md | `HEL-底层模型与话题母线` |
| KB2-概念转译对照表.md | `HEL-概念转译对照表` |
| KB3-脚本模板与视觉风格.md | `HEL-脚本模板与视觉风格` |

处理方式选 **Automatic**，其余默认，点 **Save & Process**。

---

### 第二步：导入 6 个 Agent

进入 Dify → **Studio** → 点击 **Import DSL file**

将 `dsl/` 目录下的 6 个 `.yml` 文件**依次拖入**，每个文件自动创建一个 Agent。

---

### 第三步：给 Agent 挂载知识库

每个 Agent 创建后，进入编辑页面 → **Context** → **Add** → 选择对应知识库：

| Agent | 挂载知识库 |
| :--- | :--- |
| HEL-选题Agent | KB1 + KB2 |
| HEL-脚本Agent | KB2 + KB3 |
| HEL-视觉Agent | KB3 |
| HEL-视频Agent | 无需挂载 |
| HEL-复盘Agent | 无需挂载 |
| HEL-总控Agent | 无需挂载 |

---

## 使用方式

搭建完成后，**只需打开「HEL-总控Agent」对话**，其他 5 个 Agent 作为后台专家备用。

直接输入你的观察，例如：

> 「我观察到很多人下班回家后，明明很累，却不愿意去床上睡觉，就赖在沙发上刷手机。目标平台：小红书」

总控 Agent 会自动引导你完成选题 → 脚本 → 视觉/视频方案 → 复盘的完整流程。

---

## 注意事项

1. **先调试子 Agent**：建议先单独测试选题 Agent 和脚本 Agent，确认输出质量满意后再使用总控 Agent。
2. **知识库持续投喂**：后续把你写的爆款文案、金句加入 KB2 和 KB3，Agent 会越来越像你的风格。
3. **视频 API 后期接入**：视觉/视频 Agent 目前输出提示词，实际调用可灵/火山引擎 TTS 需要在 Dify Tools 里另行配置。
4. **模型建议**：脚本 Agent 建议换用 Claude 3.5 Sonnet（金句质量更好），其余用 DeepSeek Chat 即可。
