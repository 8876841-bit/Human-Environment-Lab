"""
脚本 Agent
根据选题生成 1 分钟视频脚本
"""
from api.llm import llm


class ScriptAgent:
    """脚本 Agent"""

    SYSTEM_PROMPT = """你是 Human-Environment-Lab 的内容脚本专家。

根据给定的选题，生成一个 1 分钟短视频的完整脚本。

## 风格要求
- 时长：60 秒（约 180-200 字中文）
- 调性：轻盈、有深度、能深入人心
- 禁止：AI 腔、套话、说教

## 脚本结构
开头（0-5秒）：钩子，让人停下来
第一段（5-20秒）：提出问题或现象
第二段（20-40秒）：深入分析或故事
第三段（40-55秒）：核心观点
结尾（55-60秒）：留白或引发思考的问题

## 输出格式
直接输出 JSON，格式：
{"title": "标题", "duration": "60秒", "structure": {"opening": {"time": "0-5秒", "content": "内容类型", "text": "具体文字"}, "body1": {...}, "body2": {...}, "body3": {...}, "ending": {...}}, "style": {"tone": "风格", "pace": "节奏"}, "bgm": "BGM建议"}

只需输出 JSON，不要其他内容。"""

    def run(self, topic_result: dict) -> dict:
        """执行脚本生成"""
        selected_topic = topic_result['topics'][0]

        prompt = f"""{self.SYSTEM_PROMPT}

选题：{selected_topic['title']}
描述：{selected_topic['description']}"""

        print(f"\n📝 脚本 Agent 开始工作...")
        print(f"   选题：{selected_topic['title']}")

        result = llm.generate_json(prompt)
        result['source_topic'] = selected_topic

        print(f"   ✅ 脚本生成完成")

        return result


def create_script_agent():
    return ScriptAgent()