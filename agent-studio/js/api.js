/**
 * API 调用模块
 * 统一管理所有外部 API 调用
 */

const API = {
  /**
   * OpenAI API 调用
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
   * OpenAI DALL-E 图片生成
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
   * 通义万相 API 调用
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
   * 可灵 API - 获取 Token
   */
  async klingAuth() {
    const key = Store.getApiKey('kling');
    if (!key) throw new Error('未配置可灵 API Key');

    // 可灵使用 AK/SK 获取 Access Token
    const [ak, sk] = key.split(',');
    if (!ak || !sk) throw new Error('可灵 API Key 格式错误，应为 AK,SK');

    const response = await fetch('https://openapi.klingai.com/v1/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ak, sk })
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
    const { duration = 5, aspect_ratio = '16:9', model = 'kling-v1' } = options;

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
   * 统一出图接口（优先使用 OpenAI DALL-E，备选通义万相）
   */
  async generateImage(prompt, options = {}) {
    const openaiKey = Store.getApiKey('openai');
    const dashscopeKey = Store.getApiKey('dashscope');

    if (openaiKey) {
      return await this.dalle(prompt, options);
    } else if (dashscopeKey) {
      return await this.dashscope(prompt, options);
    } else {
      throw new Error('请至少配置 OpenAI 或通义万相 API Key');
    }
  }
};

// 暴露到全局
window.API = API;