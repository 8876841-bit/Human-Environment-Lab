"""选题01｜5镜动态版——Ken Burns效果"""
import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import Resize

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v

IMG = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
AUD = "/Users/wqq/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_3xc0tvoukv9322_bee8/msg/file/2026-06/建材市场的声音.m4a"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_动态.mp4"

audio = AudioFileClip(AUD)
imgs = sorted([f for f in os.listdir(IMG) if f.startswith("2026年6月19日")])

RES = (1920, 1080)

def ken_burns(img_path, duration, start_zoom=1.0, end_zoom=1.04, pan_x=0, pan_y=0):
    """Create a clip with subtle zoom/pan"""
    clip = ImageClip(img_path).with_duration(duration)
    # Start slightly zoomed out, end zoomed in
    clip = clip.resized(lambda t: (
        RES[0] * (start_zoom + (end_zoom - start_zoom) * t / duration),
        RES[1] * (start_zoom + (end_zoom - start_zoom) * t / duration)
    ))
    # Center crop
    clip = clip.with_position("center")
    return clip.resized(RES)

# Shot timing
bounds = [0, 7, 16, 30, 39, audio.duration]
clips = []

# Shot 1: Ultra-slow push-in toward center (0-7s)
c = ken_burns(IMG + imgs[0], bounds[1]-bounds[0], start_zoom=1.0, end_zoom=1.04)
clips.append(c)
print(f"镜头1: {bounds[0]:.0f}-{bounds[1]:.0f}s | 极慢推近 1.00→1.04")

# Shot 2: Static — locked camera (7-16s)
c = ken_burns(IMG + imgs[1], bounds[2]-bounds[1], start_zoom=1.02, end_zoom=1.02)
clips.append(c)
print(f"镜头2: {bounds[1]:.0f}-{bounds[2]:.0f}s | 固定机位")

# Shot 3: Very slow pan simulation via zoom + slight shift (16-30s)
c = ken_burns(IMG + imgs[2], bounds[3]-bounds[2], start_zoom=1.0, end_zoom=1.03)
clips.append(c)
print(f"镜头3: {bounds[2]:.0f}-{bounds[3]:.0f}s | 极慢横移感 1.00→1.03")

# Shot 4: Completely static — the stillness IS the point (30-39s)
c = ken_burns(IMG + imgs[3], bounds[4]-bounds[3], start_zoom=1.0, end_zoom=1.0)
clips.append(c)
print(f"镜头4: {bounds[3]:.0f}-{bounds[4]:.0f}s | 完全静止")

# Shot 5: Slow tilt-up feel via zoom (39-51s)
c = ken_burns(IMG + imgs[4], bounds[5]-bounds[4], start_zoom=1.0, end_zoom=1.05)
clips.append(c)
print(f"镜头5: {bounds[4]:.0f}-{bounds[5]:.0f}s | 缓慢上摇感 1.00→1.05")

video = concatenate_videoclips(clips).with_audio(audio)
video.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
