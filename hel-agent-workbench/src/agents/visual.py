"""
画面 Agent
根据脚本生成分镜描述
"""
from api.llm import llm


class VisualAgent:
    """画面 Agent"""

    SYSTEM_PROMPT = """你是 Human-Environment-Lab 的分镜画面专家。

根据给定的脚本，生成 5 个分镜描述，用于 AI 绘图。

## 分镜要求
- 每个分镜包含：场景、主体、风格、色调、氛围、视角
- 风格：抽象艺术 + 科幻感 + 未来感 + 代入感
- 不要写实主义，偏向概念化、意象化
- 色调：深色系为主，点缀色用金色/蓝色/白色光线

## AI 绘图提示词
为每个分镜生成一个英文提示词，用于 DALL-E 或 Midjourney

## 输出格式
直接输出 JSON，格式：
{"title": "标题", "shots": [{"index": 1, "time": "0-5秒", "description": "内容类型", "visual": {"scene": "场景", "subject": "主体", "style": "风格", "color": "色调", "atmosphere": "氛围", "angle": "视角"}, "prompt": "AI绘图英文提示词"}]}

只需输出 JSON，不要其他内容。"""

    def run(self, script_result: dict) -> dict:
        """执行画面生成"""
        # 提取脚本文本
        structure = script_result['structure']
        script_text = "\n".join([
            f"{structure['opening']['time']}：{structure['opening']['text']}",
            f"{structure['body1']['time']}：{structure['body1']['text']}",
            f"{structure['body2']['time']}：{structure['body2']['text']}",
            f"{structure['body3']['time']}：{structure['body3']['text']}",
            f"{structure['ending']['time']}：{structure['ending']['text']}"
        ])

        prompt = f"""{self.SYSTEM_PROMPT}

脚本：
{script_text}"""

        print(f"\n🎨 画面 Agent 开始工作...")
        print(f"   生成 {len(script_result['structure'])} 个分镜")

        result = llm.generate_json(prompt)

        print(f"   ✅ 分镜描述生成完成")

        return result


def create_visual_agent():
    return VisualAgent()