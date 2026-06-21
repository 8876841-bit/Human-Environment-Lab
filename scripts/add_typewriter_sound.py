"""选题01｜SRT字幕 + 按字符的打字音效"""
import numpy as np
from moviepy import (
    VideoFileClip, TextClip,
    CompositeVideoClip, CompositeAudioClip, AudioArrayClip
)
from moviepy.video.tools.subtitles import SubtitlesClip

VIDEO = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_字幕版.mp4"
SRT = "/tmp/subtitles_type.srt"

# SRT from Whisper segments
srt_text = """1
00:00:00,000 --> 00:00:08,000
最可怕的，不是生意不好
而是身边的人都不好以后
大家反而不挣扎了

2
00:00:08,000 --> 00:00:14,000
我前几天去了一个供应商那里
他说，大家都在扛
扛不住的已经悄悄关了

3
00:00:14,000 --> 00:00:20,000
说这话的时候他很平静
甚至笑了一下
我坐在那，没接话

4
00:00:20,000 --> 00:00:26,000
「同行都这样」「行业没办法」
听起来是安慰自己

5
00:00:26,000 --> 00:00:30,000
其实，是在慢慢放弃行动

6
00:00:30,000 --> 00:00:40,000
很多人不是突然失败的
是在一起扛、一起等、一起说再看看
然后一个人一个人地，悄悄消失

7
00:00:40,000 --> 00:00:50,700
我还在折腾
不是因为一定能赢
是怕有一天，自己也很平静地说
没办法，大家都这样
"""
with open(SRT, "w") as f:
    f.write(srt_text)

# Load video
video = VideoFileClip(VIDEO)

# Subtitles (same style as before)
def make_txt(txt):
    return TextClip(
        text=txt,
        font="/System/Library/Fonts/STHeiti Light.ttc",
        font_size=32, color="#F5F0E0",
        stroke_color="#2A2218", stroke_width=2,
        method="caption", size=(int(video.w * 0.82), None)
    )

subs = SubtitlesClip(SRT, make_textclip=make_txt).with_position(("center", 0.76), relative=True)

# Typing sounds: one soft click per Chinese character
# Figure out which characters appear at which times
sub_lines = [
    (0.0, 8.0, "最可怕的，不是生意不好而是身边的人都不好以后大家反而不挣扎了"),
    (8.0, 14.0, "我前几天去了一个供应商那里他说，大家都在扛扛不住的已经悄悄关了"),
    (14.0, 20.0, "说这话的时候他很平静甚至笑了一下我坐在那，没接话"),
    (20.0, 26.0, "「同行都这样」「行业没办法」听起来是安慰自己"),
    (26.0, 30.0, "其实，是在慢慢放弃行动"),
    (30.0, 40.0, "很多人不是突然失败的是在一起扛、一起等、一起说再看看然后一个人一个人地，悄悄消失"),
    (40.0, 50.7, "我还在折腾不是因为一定能赢是怕有一天，自己也很平静地说没办法，大家都这样"),
]

# Generate click sounds
sr = 44100
click_len = int(sr * 0.012)
t = np.linspace(0, 0.012, click_len, False)
click_mono = (np.sin(2 * np.pi * 600 * t) * np.exp(-t * 250) * 0.05).astype(np.float32)
click = np.column_stack([click_mono, click_mono])

audio_clips = []
for start_t, end_t, text in sub_lines:
    chars = [c for c in text if c not in " ，。、「」""：；？！\n"]
    if not chars:
        continue
    char_delay = min(0.07, (end_t - start_t) / len(chars))
    for ci in range(len(chars)):
        t_click = float(start_t + ci * char_delay)
        if t_click < video.duration:
            audio_clips.append(AudioArrayClip(click, fps=sr).with_start(t_click))

print(f"字幕: 7 组")
print(f"音效: {len(audio_clips)} 个击键音")

if audio_clips:
    typing = CompositeAudioClip(audio_clips)
    final_audio = CompositeAudioClip([video.audio, typing])
else:
    final_audio = video.audio

final = CompositeVideoClip([video, subs]).with_audio(final_audio)
final.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
