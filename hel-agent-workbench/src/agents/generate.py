"""
生成 Agent
根据分镜生成图片和视频
"""
import os
import asyncio
import requests
from pathlib import Path
from api.llm import image_generator, video_generator


class GenerateAgent:
    """生成 Agent"""

    def __init__(self, output_dir: str = "./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, visual_result: dict) -> dict:
        """执行生成"""
        print(f"\n🎬 生成 Agent 开始工作...")

        images = []
        videos = []

        # 生成图片
        print(f"   🖼️ 正在生成 {len(visual_result['shots'])} 张图片...")
        for shot in visual_result['shots']:
            try:
                image_data = asyncio.run(
                    image_generator.generate(shot['prompt'])
                )
                if image_data:
                    images.append({
                        'shot_index': shot['index'],
                        'url': image_data['url'],
                        'status': 'success'
                    })
                    print(f"   ✅ 图片 {shot['index']} 生成成功")
                else:
                    images.append({
                        'shot_index': shot['index'],
                        'status': 'skipped'
                    })
            except Exception as e:
                print(f"   ❌ 图片 {shot['index']} 生成失败: {e}")
                images.append({
                    'shot_index': shot['index'],
                    'error': str(e),
                    'status': 'failed'
                })

        # 生成视频
        print(f"   🎥 正在生成 {len(visual_result['shots'])} 个视频...")
        for shot in visual_result['shots']:
            try:
                video_data = asyncio.run(
                    video_generator.generate(shot['prompt'])
                )
                if video_data:
                    videos.append({
                        'shot_index': shot['index'],
                        'url': video_data['url'],
                        'cover_url': video_data.get('cover_url', ''),
                        'status': 'success'
                    })
                    print(f"   ✅ 视频 {shot['index']} 生成成功")
                else:
                    videos.append({
                        'shot_index': shot['index'],
                        'status': 'skipped'
                    })
            except Exception as e:
                print(f"   ❌ 视频 {shot['index']} 生成失败: {e}")
                videos.append({
                    'shot_index': shot['index'],
                    'error': str(e),
                    'status': 'failed'
                })

        result = {
            'title': visual_result['title'],
            'images': images,
            'videos': videos,
            'output_dir': str(self.output_dir)
        }

        print(f"   ✅ 生成完成：{len(images)} 张图片，{len(videos)} 个视频")

        return result

    def download_assets(self, result: dict) -> dict:
        """下载生成的资源"""
        print(f"\n📥 正在下载资源...")

        saved_images = []
        saved_videos = []

        # 下载图片
        for img in result.get('images', []):
            if img['status'] == 'success':
                try:
                    path = self._download_file(img['url'], f"image_{img['shot_index']}.png")
                    saved_images.append(path)
                except Exception as e:
                    print(f"   ❌ 下载图片失败: {e}")

        # 下载视频
        for vid in result.get('videos', []):
            if vid['status'] == 'success':
                try:
                    path = self._download_file(vid['url'], f"video_{vid['shot_index']}.mp4")
                    saved_videos.append(path)
                except Exception as e:
                    print(f"   ❌ 下载视频失败: {e}")

        result['saved_images'] = saved_images
        result['saved_videos'] = saved_videos

        print(f"   ✅ 下载完成：{len(saved_images)} 张图片，{len(saved_videos)} 个视频")

        return result

    def _download_file(self, url: str, filename: str) -> str:
        """下载文件"""
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        path = self.output_dir / filename
        with open(path, 'wb') as f:
            f.write(response.content)

        return str(path)


def create_generate_agent(output_dir: str = "./results"):
    return GenerateAgent(output_dir)