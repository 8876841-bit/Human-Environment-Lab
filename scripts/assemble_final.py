"""合成最终视频——5镜动画+配音"""
import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

ANIM = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
AUDIO = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_动态.mp4"

audio = AudioFileClip(AUDIO)
total = audio.duration  # ~50.7s

# Each animated shot is 6s, need to stretch to fit
# Desired durations based on script structure
desired = [10, 11, 13, 7, total - 10 - 11 - 13 - 7]  # last fills remaining

clips = []
for i, dur in enumerate(desired, 1):
    raw = VideoFileClip(f"{ANIM}shot_{i:02d}.mp4").without_audio()
    # Slow down to fit desired duration
    speed = raw.duration / dur
    if speed != 1.0:
        raw = raw.with_speed_scaled(speed)
    clips.append(raw)
    print(f"镜头{i}: {raw.duration:.1f}s (速度x{speed:.2f})")

video = concatenate_videoclips(clips).with_audio(audio)
video.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
