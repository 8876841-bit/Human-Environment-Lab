状态：DRAFT

# 00｜视频 RAG 知识库总览

> 目标：建立 12 个视频导演知识库，使 RAG 能判断、检索、组合、输出。  
> 版本：V0.2  
> 日期：2026-06-18

---

## 1. 第一性原理：导演到底在控制什么

导演的本质不是“拍画面”，而是：

```text
在限制条件内，组织视听材料，让观众从一个状态进入另一个状态。
```

这句话还可以继续下沉。

视频不是“内容的外壳”，而是一种时间中的感知工程：

```text
画面控制看见什么。
声音控制感到什么。
剪辑控制何时理解。
结构控制记住什么。
平台控制在什么心态下接收。
行动出口控制状态变化是否落地。
```

因此，导演 Agent 不能只输出脚本或分镜。它必须控制 7 个底层变量：

| 底层变量 | 导演问题 | 可观察结果 |
|---|---|---|
| 注意力 Attention | 观众为什么停下？ | 点击、3 秒留存、开头停留 |
| 理解 Comprehension | 观众是否知道你在说什么？ | 中段留存、评论理解度、复述准确度 |
| 情绪 Emotion | 观众是否有感受？ | 点赞、评论情绪、转发 |
| 信任 Trust | 观众是否相信？ | 收藏、咨询、反驳减少、正向评论 |
| 记忆 Memory | 观众能否记住一个点？ | 搜索、复看、转述、品牌/卖点回忆 |
| 行动 Action | 观众下一步做什么？ | 评论、关注、私信、购买、预约 |
| 约束 Constraint | 当前素材、平台、预算、版权允许什么？ | 可执行性、版权安全、制作成本 |

导演 Agent 的最小判断式：

```text
视频决策 = 观众状态变化 × 平台观看场景 × 视听变量 × 真实素材约束
```

如果一个建议不能说明它影响了哪个变量，它就不是导演判断，只是审美形容词。

---

## 2. 导演 Agent 的因果链

视频 RAG 的本质不是资料库，而是导演因果系统：

```text
用户模糊意图
↓
任务识别
↓
视频类型判断
↓
平台观看场景判断
↓
观众状态变化设计
↓
主观描述翻译
↓
视听变量选择
↓
案例校准
↓
稳定格式输出
```

每一步都必须回答一个因果问题：

| 步骤 | 问题 | 错误做法 |
|---|---|---|
| 任务识别 | 用户到底要解决哪个制作问题？ | 直接泛泛给建议 |
| 类型判断 | 这个视频的胜负标准是什么？ | 广告、课程、纪录片同一套模板 |
| 平台判断 | 观众在什么心态和速度里看？ | 只说“发抖音/小红书” |
| 状态变化 | 要让观众从 A 到 B 发生什么变化？ | 只说“吸引人” |
| 风格翻译 | 主观词如何落到视听变量？ | 堆“高级、真实、电影感” |
| 变量选择 | 哪些镜头/声音/剪辑能造成这种变化？ | 只写“节奏快一点” |
| 案例校准 | 有没有被验证过的相似机制？ | 收藏案例但不拆机制 |
| 输出格式 | 下一步制作需要什么结构？ | 输出无法执行的长文 |

---

## 3. 权威资料地图

这些资料不是直接照搬进库，而是作为知识库设计的外部依据。

| 资料域 | 权威来源 | 为什么权威 | 入库方式 |
|---|---|---|---|
| 影视语言 | Yale Film Analysis：`https://filmanalysis.yale.edu/` | 大学电影分析教学资源，按 mise-en-scene、cinematography、editing、sound 拆解电影语言 | 视听变量库、案例拆解库、制作原则库 |
| RAG 知识库 | Dify Knowledge：`https://docs.dify.ai/en/use-dify/knowledge/readme` | Dify 官方知识库文档 | 知识库拆分、检索增强应用接入 |
| 数据摄取 | LlamaIndex Ingestion Pipeline：`https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/` | LlamaIndex 官方数据摄取管线说明 | 文档加载、转换、嵌入、入库流程 |
| 元数据检索 | Chroma Metadata Filtering：`https://docs.trychroma.com/docs/querying-collections/metadata-filtering` | Chroma 官方 metadata 过滤文档 | 标签字段、过滤优先级、检索策略 |
| 通用元数据 | Dublin Core Terms：`https://www.dublincore.org/specifications/dublin-core/dcmi-terms/` | 通用元数据标准 | title、creator、subject、source、date 等底层字段 |
| 视听资产元数据 | PBCore Elements：`https://pbcore.org/elements` | 公共广播领域视听元数据标准 | 素材资产、权利、贡献者、实例、存放位置 |
| 网页视频结构化数据 | Schema.org VideoObject：`https://schema.org/VideoObject` | 搜索与结构化数据通用词表 | 视频名称、描述、缩略图、时长、上传时间 |
| 图片元数据 | IPTC Photo Metadata：`https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html` | 新闻与图片行业元数据标准 | 封面、图片、AI 图资产的权利和来源字段 |
| YouTube 指标 | YouTube Impressions and Watch Time：`https://support.google.com/youtube/answer/9314486?hl=en` | YouTube 官方帮助文档 | 曝光、点击率、观看时长、流量来源复盘 |
| TikTok 推荐 | TikTok For You：`https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en` | TikTok 官方推荐系统说明 | 用户互动、视频信息、设备/账号设置信号 |
| 字幕与可访问性 | W3C Captions/Subtitles：`https://www.w3.org/WAI/media/av/captions/` | W3C Web Accessibility Initiative | 字幕、说明性字幕、无声观看与可访问性 |
| AI 视频提示词 | Google Veo Prompt Guide：`https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide` | Google 官方视频生成提示词指南 | 主体、动作、场景、风格、镜头、构图、氛围 |
| 用户旅程 | NN/g Journey Mapping：`https://www.nngroup.com/articles/customer-journey-mapping/` | 用户体验研究机构方法论 | 用户阶段、行为、想法、情绪、痛点、机会 |
| Jobs To Be Done | HBR JTBD：`https://hbr.org/2016/09/know-your-customers-jobs-to-be-done` | 商业与产品动机分析方法 | 观众为什么“雇佣”这个视频完成任务 |

说明：

```text
中文平台的“算法玄学”不直接入库为事实。
抖音、小红书、B站、视频号、快手等平台，先按公开规则、创作者后台提示、账号真实数据和可观察观看场景沉淀。
凡无法确认官方来源的判断，可信度标为 B 或 C，并写明“经验观察”。
```

---

## 4. 权威等级与灵活性规则

每条知识不是“写进来就真”。必须标权威等级：

| 等级 | 来源 | 用法 |
|---|---|---|
| A1 | 标准/官方文档 | 可作为字段、流程、合规、平台指标依据 |
| A2 | 大学/专业教学资源 | 可作为影视语言、分析框架依据 |
| B1 | 多平台、多案例稳定观察 | 可作为经验规则，但必须允许平台更新 |
| B2 | 内部项目复盘 | 可作为 HEL 自己的生产经验 |
| C | 单案例/单账号观察 | 只能作为假设，不能写成原则 |

灵活性规则：

```text
知识条目不写死为模板，而写成 Operator（算子）。
Operator 只说明：在什么条件下，使用什么视听动作，影响观众哪个变量，如何验证。
```

统一算子字段：

```yaml
operator_id: ""
trigger_condition: ""
input_state: ""
target_state: ""
action: ""
affected_variables:
  attention: ""
  comprehension: ""
  emotion: ""
  trust: ""
  memory: ""
  action: ""
constraints: []
failure_modes: []
evidence_basis: []
test_method: []
```

这样同一条知识能被组合，而不是只能被复制。

---

## 5. 12 个知识库

| 序号 | 知识库 | 解决的问题 | 核心输出 |
|---|---|---|---|
| 01 | 主观描述翻译库 | 用户说的“高级、真实、电影感”到底怎么拍 | 风格词到视听变量的映射 |
| 02 | 观众状态变化库 | 观众要从什么状态变成什么状态 | 状态转化路径 |
| 03 | 视频制作原则库 | 什么做法有效，什么做法只是好看 | 原则、禁忌、判断标准 |
| 04 | 视频任务清单库 | 用户现在到底在要哪个任务 | 任务识别和调用规则 |
| 05 | 视频类型库 | 广告、课程、纪录片、带货不能用同一套判断 | 类型目标、结构、节奏、错误 |
| 06 | 输出格式库 | RAG 最终要输出什么 | 稳定模板和字段 |
| 07 | 元数据标签库 | 怎么让检索准 | 统一标签和过滤字段 |
| 08 | 案例拆解库 | 什么案例可迁移，为什么有效 | 案例机制和迁移方法 |
| 09 | 视听变量库 | 镜头、剪辑、声音、字幕怎么组合 | 可执行变量表 |
| 10 | 平台观看场景库 | 同一内容在不同平台怎么改 | 平台心态、节奏、标题封面、转化路径 |
| 11 | 素材资产索引库 | 有什么素材能用，适合什么任务 | 可检索素材目录 |
| 12 | 提示词与工作流库 | 怎么把知识库串成生产流程 | 任务提示词和自动化工作流 |

---

## 6. 统一入库字段

所有知识条目都必须有元数据和算子字段。

```yaml
knowledge_id: ""
title: ""
summary: ""
content: ""
library_id: ""
layer: ""
authority_level: ""
operator_type: ""
causal_claim: ""
primary_category: ""
secondary_category: ""
task_tags: []
video_type_tags: []
platform_tags: []
style_tags: []
scene_tags: []
not_for: []
input_conditions: []
output_supported: []
related_cases: []
related_principles: []
related_variables: []
affected_audience_variables:
  attention: ""
  comprehension: ""
  emotion: ""
  trust: ""
  memory: ""
  action: ""
constraints: []
failure_modes: []
test_method: []
source_type: ""
source_url_or_origin: ""
confidence: ""
last_updated: ""
owner: "Human-Environment-Lab"
review_status: "draft"
```

字段解释：

| 字段 | 含义 |
|---|---|
| `knowledge_id` | 全局唯一 ID，例如 `VRAG-01-STYLE-REAL-001` |
| `library_id` | 所属知识库，例如 `KB01` |
| `layer` | 底层原则、任务、类型、平台、案例、素材、工作流 |
| `authority_level` | A1/A2/B1/B2/C |
| `operator_type` | state_change、style_translation、platform_adaptation、shot_variable、workflow 等 |
| `causal_claim` | 这条知识主张“什么动作导致什么观众变化” |
| `task_tags` | 支持哪些任务，例如 `T07 分镜设计` |
| `video_type_tags` | 适用哪些视频类型，例如 `V02 广告片` |
| `platform_tags` | 适用哪些平台，例如 `P01 抖音` |
| `style_tags` | 适用哪些风格，例如真实、克制、电影感 |
| `not_for` | 不适用场景，防止误检索 |
| `output_supported` | 能支持哪些输出格式，例如 `O01 导演方案` |
| `affected_audience_variables` | 影响注意力、理解、情绪、信任、记忆、行动中的哪些变量 |
| `constraints` | 素材、版权、平台、预算、时长、比例限制 |
| `failure_modes` | 这条知识在什么情况下会失败 |
| `test_method` | 怎么验证这条知识是否有效 |
| `source_type` | official、standard、case、internal、observation、experience |
| `confidence` | A 官方/标准；B 多源验证/稳定经验；C 单源观察；D 待验证 |
| `review_status` | draft、reviewed、active、deprecated |

---

## 7. 检索规则

### 7.1 先分类，再检索

用户输入不能直接进入向量检索。必须先判断：

```text
任务类型
视频类型
目标平台
观众状态
输出格式
```

再按 metadata 过滤，最后做语义检索。

### 7.2 检索权重

```text
任务类型 > 观众状态 > 视频类型 > 平台 > 真实素材约束 > 风格词 > 案例相似度
```

解释：

```text
任务错了，检索再准也会错。
观众状态错了，导演目标会错。
平台错了，表达节奏会错。
素材约束错了，方案不可执行。
风格词只能在任务和平台之后生效。
```

### 7.3 冲突处理

当知识冲突时，优先级为：

```text
HEL 根基与当前阶段定义
↓
用户真实素材与现实约束
↓
官方规则 / 行业标准
↓
平台真实数据
↓
内部复盘经验
↓
外部案例观察
```

---

## 8. 动态组合规则

同一个主观词在不同平台、类型、观众状态下不能给同一个答案。

示例：

```text
“更真实”
```

如果是：

```text
纪录片 / B站 / 人物故事
```

优先：

```text
现场声音、人物处境、长一点的观察镜头、真实环境关系。
```

如果是：

```text
小红书 / 产品体验 / 种草
```

优先：

```text
真实使用过程、缺点也讲、手部操作、低包装字幕、可收藏的信息结构。
```

如果是：

```text
企业官网 / 产品片 / B2B 信任
```

优先：

```text
流程证明、客户案例、团队/设备/交付过程、干净稳定的镜头和声音。
```

这就是灵活性：主观词不是直接映射到模板，而是参与推理。

---

## 9. 入库顺序

最小可用版本按这个顺序建：

```text
第一批：04 视频任务清单库、05 视频类型库、06 输出格式库、07 元数据标签库
第二批：01 主观描述翻译库、02 观众状态变化库、03 视频制作原则库、09 视听变量库
第三批：10 平台观看场景库、08 案例拆解库
第四批：11 素材资产索引库、12 提示词与工作流库
```

原因：

```text
先有任务、类型、输出、标签，RAG 才知道怎么找。
再有状态、原则、变量，导演判断才有底盘。
最后接案例、平台、素材、工作流，系统才进入真实生产。
```

---

## 10. 最小可运行链路

用户输入：

```text
“这个视频太平了，我想更真实一点，但又不能太粗糙。”
```

系统判断：

```text
任务：T06 脚本优化 / T09 镜头语言设计 / T10 剪辑节奏设计 / T14 声音音乐设计
视频类型：待用户补充，默认短视频或品牌短片
平台：待用户补充，默认信息流平台
观众初始状态：无感、滑走、缺少信任
目标状态：愿意停留、觉得真实、愿意继续看
主观词：太平、真实、不粗糙
输出格式：O01 导演方案 + O03 秒级剪辑表
```

调用：

```text
04 任务清单
05 视频类型
10 平台观看场景
02 观众状态变化
01 主观描述翻译
09 视听变量
03 制作原则
08 案例拆解
06 输出格式
```

输出：

```text
减少纯讲述
增加现场证据镜头
使用中景和细节特写建立真实感
保留同期声和环境声
剪掉空泛形容词
降低字幕包装强度
用小转折替代大煽情
```

---

## 11. 停止标准

一个知识条目可以入库，必须满足：

```text
1. 能说清楚“它解决哪个导演判断问题”。
2. 有适用场景和不适用场景。
3. 至少关联一个任务类型。
4. 至少支持一个输出格式。
5. 不是孤立观点，能连接原则、变量、案例或平台。
6. 来源和可信度明确。
7. 能说明影响了观众的哪个底层变量。
8. 能说明在什么约束下会失败。
9. 能给出验证方法。
```

不能入库的内容：

```text
空泛审美判断
未经标注的平台玄学
只适合单一案例但伪装成原则的经验
没有任务归属的素材描述
不能转成行动的形容词
```
