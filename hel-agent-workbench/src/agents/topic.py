"""
选题 Agent
根据主题生成 5 个选题
"""
from api.llm import llm


class TopicAgent:
    """选题 Agent"""

    SYSTEM_PROMPT = """你是 Human-Environment-Lab 的内容选题专家。

根据用户给定的主题，生成 5 个原创选题。

## 选题要求
- 每个选题必须能引发共鸣，有画面感，适合 1 分钟短视频
- 从「人的需求」出发，而非从热点出发
- 格式：编号 + 选题 + 一句话描述

## 输出格式
直接输出 JSON 数组，格式：
[{"id": "OBS-001", "title": "选题名称", "description": "一句话描述", "needs": ["需求层"], "system": "系统场景"}]

只需输出 JSON，不要其他内容。"""

    def run(self, topic: str) -> dict:
        """执行选题"""
        prompt = f"{self.SYSTEM_PROMPT}\n\n主题：{topic}"

        print(f"\n📌 选题 Agent 开始工作...")
        print(f"   主题：{topic}")

        topics = llm.generate_json(prompt)

        # 确保返回的是 dict 格式
        if isinstance(topics, list):
            result = {
                'count': len(topics),
                'topics': topics
            }
        else:
            result = topics

        print(f"   ✅ 生成 {result['count']} 个选题")

        return result


def create_topic_agent():
    return TopicAgent()