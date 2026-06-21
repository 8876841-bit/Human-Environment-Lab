"""选题01｜5原图+配音——Ken Burns静态版"""
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import os

IMG = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
AUD = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_静态版.mp4"

imgs = sorted([f for f in os.listdir(IMG) if f.startswith("2026年6月19日")])
audio = AudioFileClip(AUD)
T = audio.duration  # ~50.7s

# Script-based timing
bounds = [0, 7, 16, 30, 39, T]
RES = (1920, 1080)

def kb(img, dur, z1, z2):
    """Ken Burns: subtle zoom in/out"""
    c = ImageClip(img).with_duration(dur)
    c = c.resized(lambda t, z1=z1, z2=z2, d=dur: (
        RES[0] * (z1 + (z2 - z1) * t / d),
        RES[1] * (z1 + (z2 - z1) * t / d)
    ))
    c = c.with_position("center")
    return c.resized(RES)

clips = []
for i in range(5):
    p = IMG + imgs[i]
    d = bounds[i+1] - bounds[i]
    # Subtle zoom: 1.00 → 1.04 for push-in feel
    c = kb(p, d, 1.00, 1.04)
    clips.append(c)
    print(f"镜头{i+1}: {bounds[i]:.0f}-{bounds[i+1]:.0f}s ({d:.1f}s) — {imgs[i]}")

video = concatenate_videoclips(clips).with_audio(audio)
video.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
