"""合成——5镜Wan2.2动画+配音"""
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

ANIM = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
AUDIO = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"

audio = AudioFileClip(AUDIO)
T = audio.duration

# Each wan shot is 6s — stretch to fit script timing
desired = [7, 9, 14, 9, T - 7 - 9 - 14 - 9]

clips = []
for i, dur in enumerate(desired, 1):
    raw = VideoFileClip(f"{ANIM}shot_{i:02d}_wan.mp4").without_audio()
    speed = raw.duration / dur
    raw = raw.with_speed_scaled(speed)
    clips.append(raw)
    print(f"镜头{i}: 6s→{dur:.1f}s (速度x{speed:.2f})")

video = concatenate_videoclips(clips).with_audio(audio)
video.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
