"""选题01｜5图+配音合成视频"""
import os, json, requests
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

# Read API key
with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v

IMG_DIR = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
AUDIO_PATH = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
OUTPUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片.mp4"

# Get audio duration
audio = AudioFileClip(AUDIO_PATH)
total_duration = audio.duration

# Get segment timestamps from Whisper
api_key = os.getenv("OPENAI_API_KEY")
with open(AUDIO_PATH, "rb") as f:
    resp = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": ("audio.m4a", f, "audio/mp4")},
        data={"model": "whisper-1", "language": "zh", "response_format": "verbose_json"}
    )
segments = resp.json()["segments"]

# Define shot boundaries based on script structure
# Shot 1: 0 to "供应商那里" (~16s)
# Shot 2: "他说大家都在扛" to "没接话" (~16-26s)
# Shot 3: "同行都这样" to "悄悄消失" (~26-38s)
# Shot 4: "悄悄消失" silence (~38-42s)
# Shot 5: "我还在折腾" to end (~42-51s)

shot_boundaries = [0, 16, 28, 40, total_duration]

# Find images
imgs = sorted([f for f in os.listdir(IMG_DIR) if f.startswith("2026年6月19日")])
print(f"Found {len(imgs)} images")
print(f"Audio: {total_duration:.1f}s")
print(f"Shot boundaries: {shot_boundaries}")

# Create video clips for each shot
clips = []
for i in range(len(shot_boundaries) - 1):
    start = shot_boundaries[i]
    end = shot_boundaries[i + 1]
    duration = end - start

    img_path = os.path.join(IMG_DIR, imgs[i])
    clip = ImageClip(img_path).with_duration(duration)
    clips.append(clip)
    print(f"Shot {i+1}: {imgs[i]} | {start:.1f}s-{end:.1f}s | {duration:.1f}s")

# Combine
video = concatenate_videoclips(clips)
video = video.with_audio(audio)

# Render
video.write_videofile(
    OUTPUT,
    fps=24,
    codec="libx264",
    audio_codec="aac",
    preset="medium",
    threads=4
)

print(f"\n✅ 成片: {OUTPUT}")
