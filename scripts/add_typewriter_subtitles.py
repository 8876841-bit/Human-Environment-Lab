"""选题01｜打字机字幕 + 轻击键音"""
import os, numpy as np
from moviepy import (
    VideoFileClip, TextClip, CompositeVideoClip,
    CompositeAudioClip, AudioArrayClip
)

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "OPENAI" in line and "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

VIDEO = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_字幕版.mp4"
FONT = "/System/Library/Fonts/STHeiti Light.ttc"

# Subtitle lines with timestamps (from Whisper)
SUBS = [
    (0.0, 8.0, ["最可怕的，不是生意不好",
                "而是身边的人都不好以后",
                "大家反而不挣扎了"]),
    (8.0, 14.0, ["我前几天去了一个供应商那里",
                 "他说，大家都在扛",
                 "扛不住的已经悄悄关了"]),
    (14.0, 20.0, ["说这话的时候他很平静",
                  "甚至笑了一下",
                  "我坐在那，没接话"]),
    (20.0, 26.0, ["「同行都这样」「行业没办法」",
                  "听起来是安慰自己"]),
    (26.0, 30.0, ["其实，是在慢慢放弃行动"]),
    (30.0, 40.0, ["很多人不是突然失败的",
                  "是在一起扛、一起等、一起说再看看",
                  "然后一个人一个人地，悄悄消失"]),
    (40.0, 50.7, ["我还在折腾",
                  "不是因为一定能赢",
                  "是怕有一天，自己也很平静地说",
                  "没办法，大家都这样"]),
]

video = VideoFileClip(VIDEO)
W, H = video.size

# Generate typing click sound (very short, soft sine)
sample_rate = 44100
click_dur = 0.015
click_samples = int(sample_rate * click_dur)
t_click = np.linspace(0, click_dur, click_samples, False)
click_wave = np.sin(2 * np.pi * 800 * t_click) * np.exp(-t_click * 200) * 0.06
# Make stereo
click_stereo = np.column_stack([click_wave, click_wave])

def make_click():
    from moviepy import AudioArrayClip
    return AudioArrayClip(click_stereo, fps=sample_rate)

all_text_clips = []
all_audio_clips = []

for start_t, end_t, lines in SUBS:
    total_dur = end_t - start_t
    # Flatten lines into single character sequence
    chars = []
    for li, line in enumerate(lines):
        for ch in line:
            chars.append((ch, li))

    char_count = len(chars)
    if char_count == 0:
        continue

    # Each character takes ~0.04-0.06s, spread across the subtitle duration
    char_delay = min(0.06, total_dur / char_count)

    for ci, (ch, li) in enumerate(chars):
        char_start = start_t + ci * char_delay
        # Build the text visible so far — all previous chars + this one
        visible = ""
        current_line = 0
        for cj, (cc, ll) in enumerate(chars):
            if cj > ci:
                break
            if ll != current_line:
                visible += "\n"
                current_line = ll
            visible += cc

        tc = TextClip(
            text=visible.strip(),
            font=FONT, font_size=32,
            color="#F5F0E0", stroke_color="#2A2218", stroke_width=2,
            method="caption", size=(W * 0.82, None)
        )
        tc = tc.with_position(("center", H * 0.76))
        tc = tc.with_start(float(char_start))
        tc = tc.with_duration(float(end_t - char_start + 0.1))
        all_text_clips.append(tc)

        # Add click sound at each character
        click_at_time = float(char_start)
        if click_at_time < video.duration:
            ac = make_click().with_start(click_at_time)
            all_audio_clips.append(ac)

    print(f"  [{start_t:.1f}-{end_t:.1f}s] {char_count}字 x{char_delay:.3f}s")

print(f"\n字幕: {len(all_text_clips)} 个字符片段")
print(f"音效: {len(all_audio_clips)} 个击键音")

# Composite
original_audio = video.audio
if all_audio_clips:
    typing_audio = CompositeAudioClip(all_audio_clips)
    mixed_audio = CompositeAudioClip([original_audio, typing_audio])
else:
    mixed_audio = original_audio

final = CompositeVideoClip([video] + all_text_clips).with_audio(mixed_audio)
final.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
