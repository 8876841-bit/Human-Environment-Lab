"""选题01｜5镜图生视频——dmxapi Hailuo"""
import os, requests, time, base64

with open("/private/tmp/Human-Environment-Lab/.env") as f:
    for line in f:
        if "=" in line and not line.startswith("#") and line.strip():
            k, v = line.strip().split("=", 1)
            os.environ[k] = v.strip()

KEY = os.getenv("DMXAPI_API_KEY")
IMG = "/Users/wqq/Downloads/海洋板案例收集/1/2/"
OUT = "/Users/wqq/Downloads/海洋板案例收集/1/2/animated/"
os.makedirs(OUT, exist_ok=True)
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

SHOTS = [
    ("2026年6月19日 16_21_36.png", "Camera pushes in extremely slowly toward five figures on bench. Dust floats in warm afternoon light beam from left window. Five round figures perfectly still — no blinking, no breathing. Wall clock frozen. Only dust moves and camera creeps. Warm melancholy. No sudden movement."),
    ("2026年6月19日 16_21_43.png", "Locked-off static camera. Left figure's head tilts very slightly — barely perceptible micro-movement toward right figure. Right figure completely frozen. Dust floats in warm light. Movement so subtle it might be illusion."),
    ("2026年6月19日 16_21_48.png", "Camera dollies right very slowly past empty wooden seats. Remaining figures motionless, not looking at empty seats. Dust floats slower. Calendar turned page, clock still 4:10."),
    ("2026年6月19日 16_21_52.png", "Completely static shot. Five empty benches. Only movement: curtain corner barely moves from unseen draft. Dust nearly still. Absolute stillness."),
    ("2026年6月19日 16_21_55.png", "Camera tilts up slowly from shadow to face. Single figure stands, chest rises with one shallow breath — first breath in series. Curtain corner still barely moves. He is thinking."),
]

print("=== 选题01 Hailuo 图生视频 ===\n")
for i, (fname, prompt) in enumerate(SHOTS, 1):
    with open(IMG + fname, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    print(f"[{i}/5] 提交...")
    r = requests.post("https://www.dmxapi.cn/v1/video_generation", headers=H, json={
        "model": "MiniMax-Hailuo-02", "prompt": prompt,
        "image": f"data:image/png;base64,{b64}", "duration": 6, "resolution": "1080P"
    }, timeout=60)
    if r.status_code != 200:
        print(f"  ❌ {r.status_code} {r.text[:150]}\n"); continue

    tid = r.json()["task_id"]
    print(f"  task_id={tid} 轮询...")

    # Poll
    for _ in range(36):
        time.sleep(10)
        pq = requests.get(f"https://www.dmxapi.cn/v1/query/video_generation?task_id={tid}", headers={"Authorization": f"Bearer {KEY}"}, timeout=20)
        if pq.status_code == 200:
            d = pq.json()
            if d.get("status") == "Success":
                fid = d["file_id"]
                # Download — needs both file_id and task_id
                dr = requests.get(f"https://www.dmxapi.cn/v1/files/retrieve?file_id={fid}&task_id={tid}",
                    headers={"Authorization": f"Bearer {KEY}"}, timeout=20)
                if dr.status_code == 200:
                    dl_url = dr.json().get("file", {}).get("download_url", "")
                    if dl_url:
                        vdata = requests.get(dl_url, timeout=60).content
                        op = f"{OUT}shot_{i:02d}.mp4"
                        with open(op, "wb") as wf:
                            wf.write(vdata)
                        print(f"  ✅ {op}\n")
                    else:
                        print(f"  ❌ 无下载链接: {dr.text[:200]}\n")
                else:
                    print(f"  ✅ 任务完成但下载失败: {dr.status_code}\n")
                break
            elif d.get("status") == "Failed":
                print(f"  ❌ 失败\n"); break
    else:
        print(f"  ⏰ 超时\n")

print("完成。")
