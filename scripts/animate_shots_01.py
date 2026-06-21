"""选题01｜5镜图生视频——Minimax API (Director mode)"""
import os, json, requests, time, base64

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "=" in line and not line.startswith("#") and line.strip():
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

API_KEY = os.getenv("MINIMAX_API_KEY")
IMG_DIR = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
OUT_DIR = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
os.makedirs(OUT_DIR, exist_ok=True)

SHOTS = [
    {
        "img": "2026年6月19日 16_21_36.png",
        "duration": 6,
        "prompt": "[Push in] Dust particles float slowly in a warm afternoon light beam from a high left window. Five identical small round figures in gray suits sit perfectly still on a wooden bench, holding white tickets. No facial features except two tiny black dot eyes, no mouths. The wall clock is frozen. Only the dust moves and the camera creeps in. Wes Anderson symmetry, Ghibli watercolor, Hopper light.",
        "desc": "镜头1: 极慢推近 + 灰尘浮动"
    },
    {
        "img": "2026年6月19日 16_21_43.png",
        "duration": 6,
        "prompt": "[Static shot] Two small round figures sit side by side. The left figure's head tilts very very slightly — a micro-movement toward the right figure, barely perceptible. The right figure is completely frozen. Dust floats in the warm light beam. Everything else is absolute stillness. The movement is so subtle it might not be real. Ghibli watercolor texture.",
        "desc": "镜头2: 固定机位 + 微小偏头"
    },
    {
        "img": "2026年6月19日 16_21_48.png",
        "duration": 6,
        "prompt": "[Truck right] Very slow camera dolly right across empty wooden seats. Two remaining figures sit completely motionless — not looking at empty seats, not looking at each other. Dust floats in the light beam but slower than before. Wall calendar has turned one page, wall clock still at 4:10. The camera movement is as slow as a held breath. Ghibli watercolor, Hopper light.",
        "desc": "镜头3: 极慢横移 + 灰尘慢浮"
    },
    {
        "img": "2026年6月19日 16_21_52.png",
        "duration": 6,
        "prompt": "[Static shot] Five empty wooden benches. No figures. The ONLY movement: a small curtain corner near the far window moves very very slightly from an unseen draft. Dust floating so slowly it is nearly still. Absolute stillness made visible. The room is full of absence. No camera movement. Ghibli watercolor, Hopper light quality.",
        "desc": "镜头4: 完全静止 + 窗帘微动"
    },
    {
        "img": "2026年6月19日 16_21_55.png",
        "duration": 6,
        "prompt": "[Tilt up] Camera tilts up very slowly from the shadow on the bench to the figure's face. A single round figure stands beside an empty bench, holding a white ticket. His chest rises and falls with one very very shallow breath — the first breath in the series. The curtain corner still moves barely. He is thinking, not sad, not triumphant. Warm light, Ghibli watercolor, Hopper atmosphere.",
        "desc": "镜头5: 极慢上摇 + 胸腔微呼吸"
    }
]

API = "https://api.minimax.io/v1/video_generation"
QUERY = "https://api.minimax.io/v1/query/video_generation"

print("=== 选题01 图生视频 (Minimax Director) ===\n")

for i, shot in enumerate(SHOTS, 1):
    img_path = IMG_DIR + shot["img"]
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    print(f"[镜头{i}/5] {shot['desc']} ({shot['duration']}s)")

    payload = {
        "model": "I2V-01-Director",
        "prompt": shot["prompt"],
        "first_frame_image": f"data:image/png;base64,{img_b64}",
        "duration": shot["duration"],
        "resolution": "1080P",
        "prompt_optimizer": True
    }

    resp = requests.post(API, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json=payload, timeout=30)

    if resp.status_code != 200:
        print(f"  ❌ 提交失败: {resp.status_code} {resp.text[:200]}\n")
        continue

    task_id = resp.json().get("task_id", "")
    print(f"  已提交: {task_id}")

    # Poll
    for attempt in range(72):  # 6 min max
        time.sleep(5)
        poll = requests.get(f"{QUERY}?task_id={task_id}", headers={
            "Authorization": f"Bearer {API_KEY}"
        })
        if poll.status_code == 200:
            data = poll.json()
            status = data.get("status", "")
            if status == "Success":
                video_url = data.get("video_url", "")
                if video_url:
                    vdata = requests.get(video_url).content
                    outpath = f"{OUT_DIR}shot_{i:02d}.mp4"
                    with open(outpath, "wb") as f:
                        f.write(vdata)
                    print(f"  ✅ {outpath}\n")
                break
            elif status in ("Failed", "Fail"):
                print(f"  ❌ 失败: {json.dumps(data, ensure_ascii=False)[:200]}\n")
                break
            elif attempt % 6 == 5:
                print(f"  等待中... ({status})")
        else:
            print(f"  轮询错误: {poll.status_code}")

print("完成。")
