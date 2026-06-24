# DECISION｜V7 口型对接：启用 kie.ai Kling Avatar

状态：DECIDED
决策：kie.ai Kling AI Avatar — 肖像+口播 → 口型同步人物视频
时间：2026-06-22 凌晨

---

## Codex 执行指令

### 步骤0：准备素材

1. 从 OSS 获取三张肖像的签名 URL（`storage_upload.mjs` 重新签名）：
   - `codex-video/portrait-photos/2026-06-21/portrait-2026-06-21-05-cream-jacket-steps.jpg`
   - `codex-video/portrait-photos/2026-06-21/portrait-2026-06-21-02-black-suit-indoor.jpg`
   - `codex-video/portrait-photos/2026-06-21/portrait-2026-06-21-03-white-qipao.jpg`

2. 上传口播到 OSS，获取公网 URL：
   - 本地：`assets/voiceover-2026-06-21.m4a`
   - OSS key：`codex-video/audio/voiceover-2026-06-21.m4a`

### 步骤1：拆分音频 + 生成口型视频

按 V7 制作包的分段和妆造表，将 88.8s 口播拆为 7 段，每段 ≤15s：

| 段 | 时间 | 时长 | 肖像 | 口播内容起止 |
|----|------|------|------|------------|
| 1 | 0-14s | 14s | portrait-05（米色） | "好几天没更了" → "我想让AI帮我" |
| 2 | 14-28s | 14s | portrait-05（米色） | "但我真的是门外汉" → "稍微有点眉目" |
| 3 | 28-42s | 14s | portrait-02（黑西装） | "这个分身不太一样" → "它从这个根上往出长" |
| 4 | 42-56s | 14s | portrait-02（黑西装） | "所以出来的内容" → "它就多一层" |
| 5 | 56-70s | 14s | portrait-03（白旗袍） | "我不是在喂机器" → "全是AI跑出来的" |
| 6 | 70-80s | 10s | portrait-03（白旗袍） | "算是我这些天" → "第一个小成果" |
| 7 | 80-89s | 9s | portrait-03（白旗袍） | "不算什么。但是个开始。我回来了。" |

**每段调用 kie.ai Kling Avatar**：

```text
POST https://api.kie.ai/api/v1/jobs/createTask
Authorization: Bearer <kie.ai API key>

{
  "model": "kling-avatar",
  "input": {
    "image_url": "<对应肖像的OSS签名URL>",
    "audio_url": "<该段音频的OSS URL>",
    "resolution": "720p"
  }
}
```

返回 `task_id`，轮询 `GET /api/v1/jobs/recordInfo?taskId={taskId}` 直到 `status: "completed"`，取 `output.video_url`。

### 步骤2：生成补充画面

按 V7 制作包的逐句画面表，生成所有补充画面（无需口型同步，Seedance / LiblibAI 即可）：

14个补充画面：日历划页、文档堆叠、分身剪影+气泡、网状裂缝、传送带+灰盒子、种子→根、年轮叠化、贩卖机、幼苗+泉水、剪辑时间轴、API日志滚动、计数器、日历自动填充、文字动画。

### 步骤3：合成

按 V7 的 A/B/C 人物布局规则，将7段口型人物视频 + 14个补充画面 + 字幕 + BGM 组装。

---

## 给用户的一句话

kie.ai Kling Avatar 已对接。Codex 现在开始拆分音频、逐段生成带口型的人物视频。7段跑完约需 10-15 分钟。
