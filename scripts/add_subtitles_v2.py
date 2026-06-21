"""选题01｜字幕烧录V2——修复版"""
import os, requests, json
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "OPENAI" in line and "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

AUDIO = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
VIDEO = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_字幕版.mp4"

# 1. Segment-level timestamps (more reliable than word-level for grouping)
print("Whisper 段级时间轴...")
with open(AUDIO, "rb") as f:
    resp = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        files={"file": ("audio.m4a", f, "audio/mp4")},
        data={"model": "whisper-1", "language": "zh", "response_format": "verbose_json"}
    )
segs = resp.json()["segments"]
print(f"   {len(segs)} 段")

# 2. Manual subtitle lines — from script, mapped to segments
# Map each segment's text to the closest script line
SUBS = [
    # (start, end, text)
    (2.3, 4.8, "最可怕的，不是生意不好"),
    (4.8, 7.5, "而是身边的人都不好以后"),
    (7.5, 9.5, "大家反而不挣扎了"),
    (9.5, 11.5, "我前几天去了一个供应商那里"),
    (11.5, 14.0, "他说，大家都在扛"),
    (14.0, 16.5, "扛不住的已经悄悄关了"),
    (16.5, 18.5, "说这话的时候他很平静"),
    (18.5, 21.0, "甚至笑了一下"),
    (21.0, 23.5, "我坐在那，没接话"),
    (23.5, 27.5, "「同行都这样」「行业没办法」"),
    (27.5, 31.0, "听起来是安慰自己"),
    (31.0, 34.0, "其实是在慢慢放弃行动"),
    (34.0, 37.0, "很多人不是突然失败的"),
    (37.0, 40.5, "是在一起扛、一起等、一起说再看看"),
    (40.5, 45.0, "然后一个人一个人地，悄悄消失"),
    (45.0, 48.0, "我还在折腾"),
    (48.0, 50.5, "不是因为一定能赢"),
    (50.5, 54.0, "是怕有一天，自己也很平静地说"),
    (54.0, 56.0, "没办法，大家都这样"),
]

# 3. Render subtitles
video = VideoFileClip(VIDEO)
W, H = video.size
sub_clips = []

for start, end, text in SUBS:
    dur = end - start
    if dur < 0.8:  # too short, skip or merge
        dur = 1.0

    tc = TextClip(
        text=text,
        font="/System/Library/Fonts/Supplemental/Songti.ttc",
        font_size=38,
        color="#F5F0E0",
        stroke_color="#4A3F35",
        stroke_width=2,
        size=(W * 0.82, None),
        method="caption"
    )
    tc = (tc
          .with_position(("center", H * 0.76))
          .with_start(start)
          .with_duration(dur))
    sub_clips.append(tc)
    print(f"  [{start:.1f}-{end:.1f}] {text}")

final = CompositeVideoClip([video] + sub_clips).with_audio(video.audio)
final.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
