/**
 * API 配置
 * 从 .env 文件加载（需要通过构建工具注入）
 * 开发时可以将配置存储在 localStorage
 */

window.ENV_CONFIG = {
  // 文本生成（优先级：DeepSeek > Claude > OpenAI）
  DEEPSEEK_API_KEY: '',
  CLAUDE_API_KEY: '',
  OPENAI_API_KEY: '',

  // 图片生成
  DASHSCOPE_API_KEY: '',

  // 视频生成
  KLING_ACCESS_KEY: '',
  KLING_SECRET_KEY: '',

  // 语音合成
  VOLC_TTS_APPID: '',
  VOLC_TTS_TOKEN: '',
  VOLC_TTS_VOICE_TYPE: 'S_N93UWQr52'
};

// 尝试从 localStorage 加载已保存的配置
(function() {
  try {
    const stored = localStorage.getItem('hel_env_config');
    if (stored) {
      const config = JSON.parse(stored);
      Object.assign(window.ENV_CONFIG, config);
    }
  } catch (e) {
    console.warn('加载环境配置失败:', e);
  }
})();

// 保存配置到 localStorage
window.saveEnvConfig = function(config) {
  localStorage.setItem('hel_env_config', JSON.stringify(config));
  Object.assign(window.ENV_CONFIG, config);
};