/**
 * API 调用模块 v2
 * 使用专业 API，优先级：
 * - 文本生成：DeepSeek > Claude > OpenAI
 * - 图片生成：DALL-E 3 > 通义万相
 * - 视频生成：可灵 + Claude
 * - 语音合成：火山引擎 TTS
 */

const API = {
  // ===== 文本生成 =====

  /**
   * DeepSeek（首选，便宜且专业）
   */
  async deepseek(prompt, options = {}) {
    const key = Store.getApiKey('deepseek');
    if (!key) throw new Error('未配置 DeepSeek API Key');

    const { model = 'deepseek-chat', max_tokens = 2000, temperature = 0.7 } = options;

    const response = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens,
        temperature
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || 'DeepSeek API 请求失败');
    }

    const data = await response.json();
    return data.choices[0].message.content;
  },

  /**
   * Claude（备选，质量高）
   */
  async claude(prompt, options = {}) {
    const key = Store.getApiKey('claude');
    if (!key) throw new Error('未配置 Claude API Key');

    const { model = 'claude-sonnet-4-20250514', max_tokens = 2000 } = options;

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': key,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model,
        max_tokens,
        messages: [{ role: 'user', content: prompt }]
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || 'Claude API 请求失败');
    }

    const data = await response.json();
    return data.content[0].text;
  },

  /**
   * OpenAI（备选）
   */
  async openai(prompt, options = {}) {
    const key = Store.getApiKey('openai');
    if (!key) throw new Error('未配置 OpenAI API Key');

    const { model = 'gpt-4o', max_tokens = 2000, temperature = 0.7 } = options;

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens,
        temperature
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || 'OpenAI API 请求失败');
    }

    const data = await response.json();
    return data.choices[0].message.content;
  },

  /**
   * 统一文本生成（自动选择可用 API）
   */
  async generateText(prompt, options = {}) {
    const deepseekKey = Store.getApiKey('deepseek');
    const claudeKey = Store.getApiKey('claude');
    const openaiKey = Store.getApiKey('openai');

    if (deepseekKey) {
      try {
        return await this.deepseek(prompt, { ...options, model: 'deepseek-chat' });
      } catch (e) {
        console.warn('DeepSeek 失败，尝试其他 API:', e.message);
      }
    }

    if (claudeKey) {
      try {
        return await this.claude(prompt, options);
      } catch (e) {
        console.warn('Claude 失败，尝试其他 API:', e.message);
      }
    }

    if (openaiKey) {
      try {
        return await this.openai(prompt, options);
      } catch (e) {
        console.warn('OpenAI 失败:', e.message);
      }
    }

    throw new Error('请至少配置一个文本生成 API（DeepSeek/Claude/OpenAI）');
  },

  // ===== 图片生成 =====

  /**
   * OpenAI DALL-E 3（首选，高质量）
   */
  async dalle(prompt, options = {}) {
    const key = Store.getApiKey('openai');
    if (!key) throw new Error('未配置 OpenAI API Key');

    const { model = 'dall-e-3', size = '1024x1024', quality = 'standard', n = 1 } = options;

    const response = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model,
        prompt,
        size,
        quality,
        n
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || 'DALL-E API 请求失败');
    }

    const data = await response.json();
    return data.data[0];
  },

  /**
   * 通义万相（备选，免费额度）
   */
  async dashscope(prompt, options = {}) {
    const key = Store.getApiKey('dashscope');
    if (!key) throw new Error('未配置通义万相 API Key');

    const { model = 'wanx-plus', size = '1024*1024' } = options;

    const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model_name: model,
        prompt,
        size,
        steps: 20
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error?.message || '通义万相 API 请求失败');
    }

    const data = await response.json();

    // 通义万相是异步的，需要轮询获取结果
    if (data.output?.task_id) {
      return await this.pollDashScopeResult(data.output.task_id, key);
    }

    return data;
  },

  /**
   * 轮询通义万相结果
   */
  async pollDashScopeResult(taskId, key, maxAttempts = 60) {
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise(resolve => setTimeout(resolve, 2000));

      const response = await fetch(
        `https://dashscope.aliyuncs.com/api/v1/tasks/${taskId}`,
        { headers: { 'Authorization': `Bearer ${key}` } }
      );

      const data = await response.json();

      if (data.output?.task_status === 'succeeded') {
        return { url: data.output.image_url };
      }

      if (data.output?.task_status === 'failed') {
        throw new Error('图片生成失败');
      }
    }

    throw new Error('图片生成超时');
  },

  /**
   * 统一图片生成
   */
  async generateImage(prompt, options = {}) {
    const openaiKey = Store.getApiKey('openai');
    const dashscopeKey = Store.getApiKey('dashscope');

    if (openaiKey) {
      try {
        return await this.dalle(prompt, options);
      } catch (e) {
        console.warn('DALL-E 失败，尝试通义万相:', e.message);
      }
    }

    if (dashscopeKey) {
      try {
        return await this.dashscope(prompt, options);
      } catch (e) {
        console.warn('通义万相失败:', e.message);
      }
    }

    throw new Error('请至少配置 OpenAI 或通义万相 API Key');
  },

  // ===== 视频生成 =====

  /**
   * 可灵（首选）
   */
  async klingAuth() {
    const key = Store.getApiKey('kling');
    if (!key) throw new Error('未配置可灵 API Key');

    // 可灵使用 AK/SK 获取 Access Token
    const accessKey = Store.getApiKey('kling_access');
    const secretKey = Store.getApiKey('kling_secret');

    if (!accessKey || !secretKey) {
      throw new Error('可灵 API Key 格式错误，应配置 access_key 和 secret_key');
    }

    const response = await fetch('https://openapi.klingai.com/v1/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ak: accessKey, sk: secretKey })
    });

    if (!response.ok) throw new Error('可灵认证失败');

    const data = await response.json();
    return data.access_token;
  },

  /**
   * 可灵 - 文生视频
   */
  async klingTextToVideo(prompt, options = {}) {
    const token = await this.klingAuth();
    const { duration = 5, aspect_ratio = '1:1', model = 'kling-v1' } = options;

    const response = await fetch('https://openapi.klingai.com/v1/videos/text2video', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        model_name: model,
        prompt,
        duration,
        aspect_ratio,
        extra: { upscape_strength: 0.4 }
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.message || '可灵 API 请求失败');
    }

    const data = await response.json();

    // 轮询视频结果
    if (data.task_id) {
      return await this.pollKlingResult(data.task_id, token);
    }

    return data;
  },

  /**
   * 轮询可灵视频结果
   */
  async pollKlingResult(taskId, token, maxAttempts = 60) {
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise(resolve => setTimeout(resolve, 3000));

      const response = await fetch(
        `https://openapi.klingai.com/v1/videos/${taskId}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      const data = await response.json();

      if (data.video?.status === 'completed') {
        return { url: data.video.url, cover_url: data.video.cover_url };
      }

      if (data.video?.status === 'failed') {
        throw new Error('视频生成失败');
      }
    }

    throw new Error('视频生成超时');
  },

  /**
   * Claude 视频生成（备选）
   */
  async claudeVideo(prompt, options = {}) {
    const key = Store.getApiKey('claude');
    if (!key) throw new Error('未配置 Claude API Key');

    const { model = 'video-01', duration = 5 } = options;

    const response = await fetch('https://api.claude.chat/v1/video creation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model,
        prompt,
        duration
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.message || 'Claude API 请求失败');
    }

    const data = await response.json();
    return data;
  },

  /**
   * 统一视频生成
   */
  async generateVideo(prompt, options = {}) {
    const klingKey = Store.getApiKey('kling_access');
    const claudeKey = Store.getApiKey('claude');

    if (klingKey) {
      try {
        return await this.klingTextToVideo(prompt, options);
      } catch (e) {
        console.warn('可灵失败，尝试 Claude:', e.message);
      }
    }

    if (claudeKey) {
      try {
        return await this.claudeVideo(prompt, options);
      } catch (e) {
        console.warn('Claude 失败:', e.message);
      }
    }

    throw new Error('请配置可灵或 Claude API Key');
  },

  // ===== 语音合成 =====

  /**
   * 火山引擎 TTS
   */
  async volcTts(text, options = {}) {
    const { appid, token, cluster = 'volcano_icl', voice_type = 'S_N93UWQr52' } = Store.getVolcTtsConfig();

    if (!appid || !token) {
      throw new Error('请配置火山引擎 TTS API Key');
    }

    const response = await fetch('https://openspeech.bytedance.com/api/v1/tts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token,
        'appid': appid,
        'cluster': cluster
      },
      body: JSON.stringify({
        text,
        voice_type: parseInt(voice_type.split('_')[1]) || 93,
        speed: 1.0,
        pitch: 1.0,
        volume: 1.0
      })
    });

    if (!response.ok) {
      throw new Error('火山引擎 TTS 请求失败');
    }

    const data = await response.json();
    return data;
  },

  // ===== 工具方法 =====

  /**
   * 加载 .env 配置
   * 注：浏览器端无法直接读取 .env，需要通过构建工具注入
   * 这里检查是否有全局配置
   */
  loadEnvConfig() {
    if (typeof window.ENV_CONFIG !== 'undefined') {
      Object.keys(window.ENV_CONFIG).forEach(key => {
        Store.saveApiKey(key, window.ENV_CONFIG[key]);
      });
    }
  },

  /**
   * 获取 API 配置状态
   */
  getStatus() {
    return {
      text: {
        deepseek: !!Store.getApiKey('deepseek'),
        claude: !!Store.getApiKey('claude'),
        openai: !!Store.getApiKey('openai')
      },
      image: {
        dalle: !!Store.getApiKey('openai'),
        dashscope: !!Store.getApiKey('dashscope')
      },
      video: {
        kling: !!Store.getApiKey('kling_access'),
        claude: !!Store.getApiKey('claude')
      },
      tts: {
        volc: !!(Store.getApiKey('volc_appid') && Store.getApiKey('volc_token'))
      }
    };
  }
};

// 暴露到全局
window.API = API;