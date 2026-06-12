"""
HEL Agent Workbench
多 Agent 内容生产流水线 - 主入口
"""
import os
import sys
import json
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.topic import create_topic_agent
from src.agents.script import create_script_agent
from src.agents.visual import create_visual_agent
from src.agents.generate import create_generate_agent
from src.utils.config import config


class Workbench:
    """工作台"""

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or config.results_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.topic_agent = create_topic_agent()
        self.script_agent = create_script_agent()
        self.visual_agent = create_visual_agent()
        self.generate_agent = create_generate_agent(str(self.output_dir))

        self.result = {}

    def run(self, topic: str, skip_generate: bool = False) -> dict:
        """运行完整流水线"""
        print("\n" + "="*60)
        print("🚀 HEL Agent Workbench 开始运行")
        print("="*60)
        print(f"\n📌 主题：{topic}")
        print(f"📁 输出目录：{self.output_dir}")
        print(f"🔑 API Provider：{self._get_provider()}")

        start_time = time.time()

        # 1. 选题
        print("\n" + "-"*60)
        topic_result = self.topic_agent.run(topic)
        self.result['topic'] = topic_result
        self._print_topics(topic_result)

        # 2. 脚本
        print("\n" + "-"*60)
        script_result = self.script_agent.run(topic_result)
        self.result['script'] = script_result
        self._print_script(script_result)

        # 3. 画面
        print("\n" + "-"*60)
        visual_result = self.visual_agent.run(script_result)
        self.result['visual'] = visual_result
        self._print_shots(visual_result)

        # 4. 生成
        if not skip_generate:
            print("\n" + "-"*60)
            generate_result = self.generate_agent.run(visual_result)
            self.result['generate'] = generate_result

            # 下载资源
            self.result['generate'] = self.generate_agent.download_assets(generate_result)

        # 保存结果
        self._save_result()

        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print(f"✅ 完成！耗时 {elapsed:.1f} 秒")
        print("="*60)

        return self.result

    def _get_provider(self) -> str:
        """获取使用的 API"""
        from src.api.llm import llm
        return llm.provider.upper()

    def _print_topics(self, result: dict):
        """打印选题"""
        print(f"\n📋 选题结果（共 {result['count']} 个）：")
        for topic in result['topics']:
            print(f"\n  [{topic['id']}] {topic['title']}")
            print(f"     {topic['description']}")

    def _print_script(self, result: dict):
        """打印脚本"""
        print(f"\n📝 脚本：{result['title']}")
        print(f"   时长：{result['duration']}")
        print(f"   风格：{result['style']['tone']}")

        structure = result['structure']
        print(f"\n   📌 开头（{structure['opening']['time']}）")
        print(f"      {structure['opening']['text']}")
        print(f"\n   📌 第一段（{structure['body1']['time']}）")
        print(f"      {structure['body1']['text']}")
        print(f"\n   📌 第二段（{structure['body2']['time']}）")
        print(f"      {structure['body2']['text']}")
        print(f"\n   📌 第三段（{structure['body3']['time']}）")
        print(f"      {structure['body3']['text']}")
        print(f"\n   📌 结尾（{structure['ending']['time']}）")
        print(f"      {structure['ending']['text']}")

        print(f"\n   🎵 BGM：{result['bgm']}")

    def _print_shots(self, result: dict):
        """打印分镜"""
        print(f"\n🎬 分镜（共 {len(result['shots'])} 个）：")
        for shot in result['shots']:
            print(f"\n  📹 分镜 {shot['index']}（{shot['time']}）")
            print(f"     描述：{shot['description']}")
            visual = shot['visual']
            print(f"     场景：{visual['scene']}")
            print(f"     风格：{visual['style']}")
            print(f"     色调：{visual['color']}")
            print(f"     氛围：{visual['atmosphere']}")
            print(f"\n     💬 AI绘图提示词：")
            print(f"        {shot['prompt'][:100]}...")

    def _save_result(self):
        """保存结果到文件"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"result_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 结果已保存：{filename}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python src/index.py <主题>")
        print("示例：python src/index.py '独居人的厨房收纳哲学'")
        print("\n选项：")
        print("  --skip-generate    跳过图片/视频生成，只生成脚本")
        sys.exit(1)

    topic = sys.argv[1]
    skip_generate = '--skip-generate' in sys.argv

    workbench = Workbench()
    workbench.run(topic, skip_generate=skip_generate)


if __name__ == "__main__":
    main()