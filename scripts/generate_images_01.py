"""选题01｜5镜图像生成脚本"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

PROMPTS = [
    # 镜头1：等候室全景，五个小人
    """A 16:9 wide hand-painted watercolor illustration. A quiet waiting room with cream walls, light yellow wainscoting, dark wooden floor. A large round wall clock frozen at 4:10. Afternoon sunlight streams from a high left window, dust particles floating slowly in the beam.

Five identical round small figures sit on a long wooden bench facing forward. Soft gray suits, each holding a white number ticket. Minimal faces: only two tiny black dot eyes, no mouth. Perfectly still, eerily calm. Strictly symmetrical composition.

Style: Wes Anderson precise symmetry, Studio Ghibli watercolor texture with visible paper grain, Edward Hopper light quality. Warm palette but the warmth feels thin — like late afternoon light that knows it's leaving. No text. No mouths on figures.""",

    # 镜头2：两个小人，一个侧头"说话"
    """Same waiting room, same light, same color palette, same watercolor style. 16:9 wide.

Medium close-up. Two round small figures sit side by side. The left figure tilts his head slightly toward the right one — as if speaking — but his face has no mouth. The right figure stares straight ahead, completely still. The left figure's white number ticket hangs loose in his hand, ungripped.

Dust still floating in the light beam. Camera locked off — the viewer is a silent third person on this bench. Same Wes Anderson + Ghibli watercolor + Hopper light style. No text.""",

    # 镜头3：人少了，空椅子
    """Same waiting room, same light, same palette, same watercolor style. 16:9 wide shot.

The same long bench. But now only two figures remain. Three empty seats between them, evenly spaced. White number tickets lie abandoned on the empty seats. An old wall calendar has turned one page. But the large round clock is still at 4:10.

Dust floating slower than before. The two remaining figures completely motionless — not looking at the empty seats, not looking at each other. The silence in the room has thickened.

Wes Anderson symmetry, Ghibli watercolor, Hopper light. No text.""",

    # 镜头4：空椅子
    """Same waiting room, same light direction, same muted warm palette, same watercolor style. 16:9 wide.

Five empty wooden benches receding from near to far. No figures at all. A white number ticket lies under each bench — dropped, forgotten. The wall clock frozen at 4:10.

Afternoon light beam still coming through the high left window. Dust floating so slowly it is nearly still.

At the far right, near the window, a small curtain corner moves — just barely — from a sliver of wind through a crack in the window. This is the ONLY visible motion in the entire frame.

The room is full of absence. Ghibli watercolor, Wes Anderson composition, Hopper light quality. No text. No figures.""",

    # 镜头5：一个人站着，在看空椅子
    """Same waiting room, same light, same palette, same watercolor style. 16:9 wide.

A single empty wooden bench. Beside it, one round small figure in a soft gray suit stands. He is not sitting. His body is turned toward the empty bench, facing it. His white number ticket is still in his hand. His tiny black dot eyes look at the empty bench — not sad, not triumphant, but thinking. Someone in the middle of a decision.

Warm afternoon light from the left casts his long shadow across the empty bench. His chest rises and falls very very slightly — the first figure in the entire series who is breathing.

The curtain corner moves again — barely, from that same sliver of wind. The wall clock still at 4:10.

Ghibli watercolor, Wes Anderson composition, Hopper light. No text."""
]

OUTPUT_DIR = "outputs/topic01"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 50)
print("选题01｜5镜图像生成")
print("=" * 50)

for i, prompt in enumerate(PROMPTS, 1):
    shot_num = i
    print(f"\n[镜头 {shot_num}/5] 生成中...")

    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-image-1",
            "prompt": prompt,
            "size": "1792x1024",
            "n": 1
        },
        timeout=120
    )

    if resp.status_code == 200:
        data = resp.json()
        img_url = data["data"][0]["url"]
        # download image
        img_data = requests.get(img_url).content
        filepath = f"{OUTPUT_DIR}/shot_{shot_num:02d}.png"
        with open(filepath, "wb") as f:
            f.write(img_data)
        print(f"  ✅ 已保存: {filepath}")
    else:
        print(f"  ❌ 失败: {resp.status_code} {resp.text[:200]}")

print(f"\n全部完成。图片在: {OUTPUT_DIR}/")
