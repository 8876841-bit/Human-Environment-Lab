"""选题01｜5镜图生视频——DashScope Wan2.7-I2V"""
import os, requests, time, base64

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "DASHSCOPE" in line and "=" in line and not line.startswith("#") and line.strip():
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

KEY = os.getenv("DASHSCOPE_API_KEY")
API = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
IMG = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
os.makedirs(OUT, exist_ok=True)

H = {
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}

SHOTS = [
    ("2026年6月19日 16_21_36.png", "The camera pushes in extremely slowly. Dust particles float gently in the warm afternoon light beam. Five identical figures sit perfectly still on the bench — no blinking, no breathing. The wall clock is frozen. Only the dust in the light beam moves. The atmosphere is warm but melancholic. Preserve the original watercolor texture and Wes Anderson composition exactly."),
    ("2026年6月19日 16_21_43.png", "The left figure's head tilts very very slightly to the right — a barely perceptible micro-movement, as if about to whisper but remaining silent. The right figure stays completely frozen. Everything else is absolute stillness. The movement is so subtle it might be an optical illusion. Watercolor texture preserved."),
    ("2026年6月19日 16_21_48.png", "Preserve watercolor style. Camera dollies right extremely slowly across empty seats. The two remaining figures are completely motionless — they don't look at empty seats or each other. Dust floats slower now. Calendar has turned one page, clock frozen."),
    ("2026年6月19日 16_21_52.png", "Completely static. Five empty benches. Only movement: a curtain corner near the window moves very very slightly from an unseen draft. Everything else frozen. Watercolor texture exactly preserved."),
    ("2026年6月19日 16_21_55.png", "Camera tilts up very slowly from shadow to face. The single standing figure takes one very shallow breath — his chest barely rises and falls. The first breath in the series. The curtain corner still barely moves. He is thinking, not sad, not triumphant. Watercolor preserved."),
]

print("=== Wan2.7 图生视频 ===\n")
for i, (fname, prompt) in enumerate(SHOTS, 1):
    with open(IMG + fname, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    print(f"[{i}/5] 提交...")
    r = requests.post(API, headers=H, json={
        "model": "wan2.7-i2v-2026-04-25",
        "input": {
            "prompt": prompt,
            "media": [{"type": "first_frame", "url": f"data:image/png;base64,{b64}"}]
        },
        "parameters": {"resolution": "720P", "duration": 6, "prompt_extend": True}
    }, timeout=60)

    if r.status_code != 200:
        print(f"  ❌ {r.status_code} {r.text[:200]}\n"); continue

    tid = r.json().get("output", {}).get("task_id", "")
    print(f"  task={tid} 轮询...")

    for _ in range(48):
        time.sleep(10)
        pq = requests.get(f"https://dashscope.aliyuncs.com/api/v1/tasks/{tid}",
            headers={"Authorization": f"Bearer {KEY}"}, timeout=20)
        if pq.status_code == 200:
            d = pq.json()
            s = d.get("output", {}).get("task_status", "")
            if s == "SUCCEEDED":
                url = d["output"]["video_url"]
                vdata = requests.get(url, timeout=60).content
                op = f"{OUT}shot_{i:02d}_ds.mp4"
                with open(op, "wb") as wf:
                    wf.write(vdata)
                print(f"  ✅ {op}\n")
                break
            elif s == "FAILED":
                print(f"  ❌ {d.get('output',{}).get('message','?')}\n"); break
            elif _ % 6 == 5:
                print(f"  等待... ({s})")
    else:
        print(f"  ⏰ 超时\n")

print("完成。")
