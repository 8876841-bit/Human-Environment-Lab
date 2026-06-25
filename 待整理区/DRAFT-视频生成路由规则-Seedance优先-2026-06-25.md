# DRAFT｜视频生成路由规则：Seedance 优先

状态：DRAFT
创建：2026-06-25
来源：人类倩倩输入

```text
视频播放优先see dance
```

系统按以下含义理解：

```text
视频生成 / 视频素材生成优先使用 Seedance 路线。
```

---

## 1. 规则定义

在内容生产多模型调度系统中，涉及 AI 视频生成、视频素材生成、动态片段生成时，默认优先选择 Seedance 路线。

优先级暂定：

```text
1. Volcengine ARK Seedance
2. LiblibAI 视频路线
3. DMXAPI.cn 视频路线
4. SiliconFlow Wan 视频路线
5. 其他视频模型路线
```

Kling official 官方直连当前暂不作为主路，原因是既有 API 审计中鉴权探测失败。

---

## 2. 适用范围

适用于：

```text
AI 视频素材生成
图生视频
文生视频
多图参考视频
内容视频中的氛围片段
口播视频中的补充画面
```

不适用于：

```text
最终剪辑合成
字幕压制
图文卡片转视频
封面图生成
普通播放器播放
```

以上任务仍优先走：

```text
ffmpeg / moviepy / Remotion / ChatGPT image2
```

---

## 3. Codex 执行规则

Codex 在执行视频生成相关任务时，应遵守：

```text
1. 生成前先调用本地 RAG 检索相关风格与规则。
2. 判断任务是否属于 AI 视频素材生成。
3. 如果属于，优先使用 Seedance 路线。
4. 如果 Seedance 失败，再进入 LiblibAI / DMXAPI.cn / SiliconFlow Wan 备选路线。
5. 每次调用必须写 generation-log。
6. 不允许自由选择高成本视频模型。
7. 不允许把失败路线静默跳过，必须记录失败原因。
```

---

## 4. 当前阶段建议

第一阶段仍建议：

```text
知识类视频 / 图文视频：优先 ffmpeg / moviepy / Remotion 合成。
AI 动态素材：优先 Seedance。
图片与关键帧：暂时优先 ChatGPT image2。
```

---

## 5. 等待确认

请人类倩倩确认是否将本规则并入后续：

```text
确认，视频生成优先 Seedance
```

确认后，再进入模型调度规则或 Codex 媒体生成执行规则的正式整合。
