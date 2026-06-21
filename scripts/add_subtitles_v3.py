"""选题01｜SRT字幕烧录V3"""
import os, requests, json
from moviepy import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "OPENAI" in line and "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

VIDEO = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_Wan版.mp4"
SRT = "/tmp/subtitles.srt"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/选题01_成片_字幕版.mp4"

# Manual SRT — script lines with timestamps
srt_lines = """1
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
我还在折腾。不是因为一定能赢
是怕有一天，自己也很平静地说
没办法，大家都这样
"""

with open(SRT, "w") as f:
    f.write(srt_lines)

def make_txt(txt):
    from moviepy import TextClip
    return TextClip(
        text=txt, font="/System/Library/Fonts/STHeiti Light.ttc",
        font_size=32, color="#F5F0E0", stroke_color="#2A2218", stroke_width=2,
        method="caption", size=(1600, None)
    )

video = VideoFileClip(VIDEO)
subs = SubtitlesClip(SRT, make_textclip=make_txt)
subs = subs.with_position(("center", 0.76), relative=True)

from moviepy import CompositeVideoClip
final = CompositeVideoClip([video, subs]).with_audio(video.audio)
final.write_videofile(OUT, fps=24, codec="libx264", audio_codec="aac", preset="medium", threads=4)
print(f"\n✅ {OUT}")
