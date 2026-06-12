"""
配置管理模块
从 config.yaml 加载配置
"""
import os
import yaml
from pathlib import Path


class Config:
    """配置类"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """加载配置文件"""
        # 配置文件在项目根目录
        config_path = Path(__file__).parent.parent.parent / "config.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)

    @property
    def deepseek_api_key(self) -> str:
        return self._config.get('deepseek_api_key', '')

    @property
    def claude_api_key(self) -> str:
        return self._config.get('claude_api_key', '')

    @property
    def openai_api_key(self) -> str:
        return self._config.get('openai_api_key', '')

    @property
    def dashscope_api_key(self) -> str:
        return self._config.get('dashscope_api_key', '')

    @property
    def kling_access_key(self) -> str:
        return self._config.get('kling_access_key', '')

    @property
    def kling_secret_key(self) -> str:
        return self._config.get('kling_secret_key', '')

    @property
    def volc_appid(self) -> str:
        return self._config.get('volc_appid', '')

    @property
    def volc_token(self) -> str:
        return self._config.get('volc_token', '')

    @property
    def volc_voice_type(self) -> str:
        return self._config.get('volc_voice_type', 'S_N93UWQr52')

    @property
    def default_model(self) -> str:
        return self._config.get('generation', {}).get('default_model', 'deepseek-chat')

    @property
    def max_tokens(self) -> int:
        return self._config.get('generation', {}).get('max_tokens', 2000)

    @property
    def temperature(self) -> float:
        return self._config.get('generation', {}).get('temperature', 0.7)

    @property
    def results_dir(self) -> str:
        return self._config.get('output', {}).get('results_dir', './results')

    def get_text_api_key(self) -> str:
        """获取可用的文本生成 API Key（优先级：DeepSeek > Claude > OpenAI）"""
        if self.deepseek_api_key:
            return self.deepseek_api_key, 'deepseek'
        if self.claude_api_key:
            return self.claude_api_key, 'claude'
        if self.openai_api_key:
            return self.openai_api_key, 'openai'
        return '', None

    def get_image_api_key(self) -> str:
        """获取可用的图片生成 API Key"""
        if self.openai_api_key:
            return self.openai_api_key, 'dalle'
        if self.dashscope_api_key:
            return self.dashscope_api_key, 'dashscope'
        return '', None


# 全局配置实例
config = Config()