"""选题01｜字幕烧录——匹配水彩风格的暖白衬线体"""
import os, requests, json
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "OPENAI" in line and "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

AUDIO = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
VIDEO = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_字幕版.mp4"

# 1. Whisper word-level timestamps
print("Whisper 词级时间轴...")
with open(AUDIO, "rb") as f:
    resp = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        files={"file": ("audio.m4a", f, "audio/mp4")},
        data={"model": "whisper-1", "language": "zh", "response_format": "verbose_json",
              "timestamp_granularities": "word"}
    )
words = resp.json().get("words", [])

# 2. Group words into subtitle lines by natural pauses (>0.5s gap = new line)
lines = []
line = {"words": [], "start": None, "end": None}
for w in words:
    t = w["start"]
    txt = w["word"].strip()
    if not txt:
        continue
    if line["start"] is None:
        line["start"] = t
    line["end"] = w["end"]
    line["words"].append(txt)
    # Break on natural pause or max line length
    if len("".join(line["words"])) >= 14:
        lines.append(line)
        line = {"words": [], "start": None, "end": None}
if line["words"]:
    lines.append(line)

# Collapse short single-word lines into previous
merged = []
for l in lines:
    if merged and len("".join(l["words"])) <= 2 and l["end"] - l["start"] < 0.6:
        merged[-1]["words"].extend(l["words"])
        merged[-1]["end"] = l["end"]
    else:
        merged.append(l)

# 3. Create subtitle clips
video = VideoFileClip(VIDEO)
W, H = video.size

# Style: warm cream, serif, subtle — matching watercolor aesthetic
def make_sub(text, start, end):
    dur = end - start
    txt = "".join(text)
    clip = (TextClip(
        text=txt, font="Helvetica", font_size=42,
        color="#F5F0E0",                # warm cream — not harsh white
        stroke_color="#3A3028", stroke_width=1.2,  # thin dark brown stroke for readability
        size=(W * 0.85, None),
        method="caption"
    )
    .with_position(("center", H * 0.78))
    .with_start(start)
    .with_duration(dur)
    .with_effects([lambda c: c.crossfadein(0.15).crossfadeout(0.15)]))
    return clip

subs = []
for l in merged:
    subs.append(make_sub(l["words"], l["start"], l["end"]))
    txt = "".join(l["words"])
    print(f"  [{l['start']:.1f}s-{l['end']:.1f}s] {txt}")

final = CompositeVideoClip([video] + subs).with_audio(video.audio)
final.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
