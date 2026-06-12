"""
LLM API 调用模块
统一管理所有文本生成 API
"""
import json
import time
import requests
from typing import Optional, Dict, Any
from utils.config import config


class LLM:
    """LLM 统一接口"""

    def __init__(self):
        self.api_key = None
        self.provider = None
        self._init_provider()

    def _init_provider(self):
        """初始化 API 提供商"""
        self.api_key, self.provider = config.get_text_api_key()
        if not self.api_key:
            raise ValueError("未配置任何文本生成 API Key")

    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if self.provider == 'deepseek':
            return self._deepseek_generate(prompt, **kwargs)
        elif self.provider == 'claude':
            return self._claude_generate(prompt, **kwargs)
        elif self.provider == 'openai':
            return self._openai_generate(prompt, **kwargs)
        else:
            raise ValueError(f"不支持的 provider: {self.provider}")

    def _deepseek_generate(self, prompt: str, **kwargs) -> str:
        """DeepSeek API"""
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": kwargs.get('model', 'deepseek-chat'),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get('max_tokens', config.max_tokens),
            "temperature": kwargs.get('temperature', config.temperature)
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    def _claude_generate(self, prompt: str, **kwargs) -> str:
        """Claude API"""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": kwargs.get('model', 'claude-sonnet-4-20250514'),
            "max_tokens": kwargs.get('max_tokens', config.max_tokens),
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()
        return result['content'][0]['text']

    def _openai_generate(self, prompt: str, **kwargs) -> str:
        """OpenAI API"""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": kwargs.get('model', 'gpt-4o'),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get('max_tokens', config.max_tokens),
            "temperature": kwargs.get('temperature', config.temperature)
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成 JSON 格式结果"""
        text = self.generate(prompt, **kwargs)
        # 尝试提取 JSON
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)


class ImageGenerator:
    """图片生成"""

    def __init__(self):
        self.api_key = None
        self.provider = None
        self._init_provider()

    def _init_provider(self):
        """初始化 API 提供商"""
        self.api_key, self.provider = config.get_image_api_key()
        if not self.api_key:
            print("⚠️ 未配置图片生成 API，跳过图片生成")
            self.provider = None

    async def generate(self, prompt: str, **kwargs):
        """生成图片"""
        if not self.provider:
            return None

        if self.provider == 'dalle':
            return await self._dalle_generate(prompt, **kwargs)
        elif self.provider == 'dashscope':
            return await self._dashscope_generate(prompt, **kwargs)
        else:
            print(f"⚠️ 不支持的图片 provider: {self.provider}")
            return None

    async def _dalle_generate(self, prompt: str, **kwargs):
        """DALL-E 3"""
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()
        return {
            'url': result['data'][0]['url'],
            'revised_prompt': result['data'][0].get('revised_prompt', '')
        }

    async def _dashscope_generate(self, prompt: str, **kwargs):
        """通义万相"""
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "wanx-plus",
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "size": "1024*1024"
            }
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        result = response.json()

        # 通义万相是异步的，需要轮询
        if result.get('output', {}).get('task_id'):
            task_id = result['output']['task_id']
            return await self._poll_dashscope_result(task_id)

        return result

    async def _poll_dashscope_result(self, task_id: str, max_attempts: int = 60):
        """轮询通义万相结果"""
        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        for i in range(max_attempts):
            time.sleep(2)
            response = requests.get(url, headers=headers, timeout=30)
            result = response.json()

            if result.get('output', {}).get('task_status') == 'succeeded':
                return {'url': result['output']['image_url']}

            if result.get('output', {}).get('task_status') == 'failed':
                raise Exception("图片生成失败")

        raise Exception("图片生成超时")


class VideoGenerator:
    """视频生成"""

    def __init__(self):
        self.access_key = config.kling_access_key
        self.secret_key = config.kling_secret_key
        self.token = None

    def _get_token(self) -> str:
        """获取可灵 access token"""
        if self.token:
            return self.token

        url = "https://openapi.klingai.com/v1/auth/token"
        headers = {"Content-Type": "application/json"}
        data = {"ak": self.access_key, "sk": self.secret_key}

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        self.token = response.json()['access_token']
        return self.token

    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成视频"""
        if not self.access_key or not self.secret_key:
            print("⚠️ 未配置可灵 API，跳过视频生成")
            return None

        token = self._get_token()
        url = "https://openapi.klingai.com/v1/videos/text2video"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "model_name": "kling-v1",
            "prompt": prompt,
            "duration": kwargs.get('duration', 5),
            "aspect_ratio": kwargs.get('aspect_ratio', '1:1')
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()

        if result.get('task_id'):
            return await self._poll_result(result['task_id'], token)

        return result

    async def _poll_result(self, task_id: str, token: str, max_attempts: int = 60):
        """轮询视频结果"""
        url = f"https://openapi.klingai.com/v1/videos/{task_id}"
        headers = {"Authorization": f"Bearer {token}"}

        for i in range(max_attempts):
            time.sleep(3)
            response = requests.get(url, headers=headers, timeout=30)
            result = response.json()

            if result.get('video', {}).get('status') == 'completed':
                return {
                    'url': result['video']['url'],
                    'cover_url': result['video'].get('cover_url', '')
                }

            if result.get('video', {}).get('status') == 'failed':
                raise Exception("视频生成失败")

        raise Exception("视频生成超时")


# 全局实例
llm = LLM()
image_generator = ImageGenerator()
video_generator = VideoGenerator()