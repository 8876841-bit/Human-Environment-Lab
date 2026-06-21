"""选题01｜5镜图生视频——SiliconFlow Wan2.2-I2V"""
import os, json, requests, time, base64

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "=" in line and not line.startswith("#") and line.strip():
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

API_KEY = os.getenv("SILICONFLOW_API_KEY")
API = "https://api.siliconflow.cn/v1/video/submit"
IMG_DIR = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
OUT_DIR = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
os.makedirs(OUT_DIR, exist_ok=True)

SHOTS = [
    ("2026年6月19日 16_21_36.png", 6,
     "Extremely slow push-in toward five figures. Dust particles float slowly in warm afternoon light beam from left window. Five identical round figures in gray suits sit perfectly still on wooden bench, no mouths, only two tiny black dot eyes. Wall clock frozen. Only dust floats and camera creeps imperceptibly. Wes Anderson symmetry, watercolor. No sudden movement.",
     "镜头1: 极慢推近+灰尘"),
    ("2026年6月19日 16_21_43.png", 6,
     "Locked-off static camera. Two figures on bench. Left figure's head tilts very very slightly — a micro-movement toward the right, barely perceptible. Right figure absolutely frozen. Dust floats in warm light. The movement is so subtle it might be an illusion. Watercolor, warm melancholy.",
     "镜头2: 微偏头"),
    ("2026年6月19日 16_21_48.png", 6,
     "Camera dollies right extremely slowly past empty wooden seats. Two remaining figures completely motionless — not looking at empty seats, not looking at each other. Dust floats slower now. Wall calendar turned one page, clock still at 4:10. Watercolor, Hopper light.",
     "镜头3: 极慢横移"),
    ("2026年6月19日 16_21_52.png", 6,
     "Completely static shot. Five empty benches. No figures. Only movement: a curtain corner barely moves — a sliver of wind through an unseen crack. Dust nearly still. Absolute stillness as subject. Watercolor, Hopper light.",
     "镜头4: 窗帘微动"),
    ("2026年6月19日 16_21_55.png", 6,
     "Camera tilts up very slowly from shadow to face. Single figure stands beside empty bench holding white ticket. His chest rises and falls with one very shallow breath — the first breath in the series. Curtain corner still barely moves. He is thinking. Warm light, watercolor.",
     "镜头5: 呼吸+上摇"),
]

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

print("=== Wan2.2 图生视频 ===\n")
for i, (img_file, dur, prompt, desc) in enumerate(SHOTS, 1):
    img_path = IMG_DIR + img_file
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    print(f"[{i}/5] {desc} ({dur}s)")
    payload = {
        "model": "Wan-AI/Wan2.2-I2V-A14B",
        "prompt": prompt,
        "image": f"data:image/png;base64,{img_b64}",
        "image_size": "1280x720",
    }

    resp = requests.post(API, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"  ❌ {resp.status_code}: {resp.text[:200]}\n")
        continue

    data = resp.json()
    request_id = data.get("requestId", "")

    if request_id:
        print(f"  任务: {request_id}, 轮询中...")
        for attempt in range(72):
            time.sleep(5)
            pq = requests.get(f"https://api.siliconflow.cn/v1/video/status/{request_id}", headers=headers)
            if pq.status_code == 200:
                pd = pq.json()
                if pd.get("status") in ("completed", "success", "done", "succeeded", "Succeeded"):
                    results = pd.get("results", [])
                    if results:
                        vurl = results[0].get("url", "")
                        if vurl:
                            vdata = requests.get(vurl).content
                            outpath = f"{OUT_DIR}shot_{i:02d}.mp4"
                            with open(outpath, "wb") as f:
                                f.write(vdata)
                            print(f"  ✅ {outpath}\n")
                        break
                    else:
                        vurl = pd.get("url") or pd.get("video_url") or ""
                        if vurl:
                            vdata = requests.get(vurl).content
                            outpath = f"{OUT_DIR}shot_{i:02d}.mp4"
                            with open(outpath, "wb") as f:
                                f.write(vdata)
                            print(f"  ✅ {outpath}\n")
                        break
                elif pd.get("status") in ("failed", "error", "Failed"):
                    print(f"  ❌ 失败: {json.dumps(pd, ensure_ascii=False)[:200]}\n")
                    break
                elif attempt % 12 == 11:
                    print(f"  等待... ({pd.get('status','?')})")
    else:
        print(f"  ⚠️ {json.dumps(data, ensure_ascii=False)[:300]}\n")

print("完成。")
