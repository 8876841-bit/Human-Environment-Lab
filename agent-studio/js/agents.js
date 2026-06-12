/**
 * 各 Agent 逻辑 v2
 * 优先使用专业 API：DeepSeek > Claude > OpenAI
 */

const Agents = {
  /**
   * 选题 Agent - 生成 5 个选题
   */
  async topicAgent(topic) {
    try {
      // 使用真实 API（自动选择可用的）
      const prompt = `你是 Human-Environment-Lab 的内容选题专家。

根据主题「${topic}」，生成 5 个原创选题。

## 选题要求
- 每个选题必须能引发共鸣，有画面感，适合 1 分钟短视频
- 从「人的需求」出发，而非从热点出发
- 格式：编号 + 选题 + 一句话描述

## 输出格式
直接输出 JSON 数组，格式：
[{"id": "OBS-001", "title": "选题名称", "description": "一句话描述", "needs": ["需求层"], "system": "系统场景"}]

只需输出 JSON，不要其他内容。`;

      const result = await API.generateText(prompt, { max_tokens: 1500 });
      const topics = JSON.parse(result);

      return {
        count: topics.length,
        topics: topics,
        source: 'deepseek',
        timestamp: new Date().toISOString()
      };
    } catch (e) {
      console.error('选题失败:', e);
      throw e;
    }
  },

  /**
   * 脚本 Agent - 生成 1 分钟视频脚本
   */
  async scriptAgent(topicResult) {
    const selectedTopic = topicResult.topics[0];

    try {
      const prompt = `你是 Human-Environment-Lab 的内容脚本专家。

选题：「${selectedTopic.title}」
描述：${selectedTopic.description}

生成一个 1 分钟短视频的完整脚本。

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

只需输出 JSON，不要其他内容。`;

      const result = await API.generateText(prompt, { max_tokens: 2000 });
      const script = JSON.parse(result);
      script.source = 'deepseek';
      script.timestamp = new Date().toISOString();
      return script;
    } catch (e) {
      console.error('脚本生成失败:', e);
      throw e;
    }
  },

  /**
   * 画面 Agent - 生成分镜描述
   */
  async visualAgent(scriptResult) {
    try {
      const scriptText = Object.values(scriptResult.structure).map(s => s.text).join('\n');

      const prompt = `你是 Human-Environment-Lab 的分镜画面专家。

根据以下脚本，生成 5 个分镜描述，用于 AI 绘图：

脚本：
${scriptText}

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

只需输出 JSON，不要其他内容。`;

      const result = await API.generateText(prompt, { max_tokens: 2500 });
      const visual = JSON.parse(result);
      visual.source = 'deepseek';
      visual.timestamp = new Date().toISOString();
      return visual;
    } catch (e) {
      console.error('画面生成失败:', e);
      throw e;
    }
  },

  /**
   * 生成 Agent - 生成图片/视频
   */
  async generateAgent(visualResult) {
    const images = [];
    const videos = [];

    // 生成图片（DALL-E 或通义万相）
    for (const shot of visualResult.shots) {
      try {
        const imageData = await API.generateImage(shot.prompt, {
          model: 'dall-e-3',
          size: '1024x1024',
          quality: 'standard'
        });
        images.push({
          shotIndex: shot.index,
          url: imageData.url,
          revised_prompt: imageData.revised_prompt,
          status: 'success'
        });
      } catch (e) {
        console.error(`图片生成失败 (分镜 ${shot.index}):`, e);
        images.push({
          shotIndex: shot.index,
          error: e.message,
          prompt: shot.prompt,
          status: 'failed'
        });
      }
    }

    // 视频生成（可灵）
    const klingKey = Store.getApiKey('kling_access');
    if (klingKey) {
      for (const shot of visualResult.shots) {
        try {
          const videoData = await API.klingTextToVideo(shot.prompt, {
            duration: 5,
            aspect_ratio: '1:1'
          });
          videos.push({
            shotIndex: shot.index,
            url: videoData.url,
            cover_url: videoData.cover_url,
            status: 'success'
          });
        } catch (e) {
          console.error(`视频生成失败 (分镜 ${shot.index}):`, e);
          videos.push({
            shotIndex: shot.index,
            error: e.message,
            status: 'failed'
          });
        }
      }
    }

    return {
      title: visualResult.title,
      images: images,
      videos: videos,
      hasImages: images.length > 0 && images[0].status === 'success',
      hasVideos: videos.length > 0 && videos[0].status === 'success',
      status: images.some(i => i.status === 'success') ? 'partial' : 'pending',
      nextSteps: [
        '1. 查看生成的图片',
        images.some(i => i.status === 'failed') ? '2. 部分图片生成失败，可重新生成' : '2. 图片生成完成',
        klingKey ? '3. 查看生成的视频' : '3. 配置可灵 API Key 生成视频',
        '4. 用剪映拼接成完整视频',
        '5. 添加 BGM 和字幕',
        '6. 发布'
      ],
      timestamp: new Date().toISOString()
    };
  },

  /**
   * 生成场景描述
   */
  getScene(index) {
    const scenes = [
      '一个空旷的房间，光线从窗户斜射进来',
      '极简的空间，几何线条勾勒出人的轮廓',
      '流动的光线穿过透明材质',
      '深色背景中浮现出抽象的人形',
      '渐亮的暖色光芒，人影逐渐清晰'
    ];
    return scenes[index] || scenes[0];
  },

  /**
   * 生成 AI 绘图提示词
   */
  getPrompt(index, part) {
    const prompts = [
      'abstract art, minimalist interior, soft light from window, geometric shapes, human silhouette, deep blue tones, cinematic, 8k, futuristic',
      'concept art, empty space, floating particles, abstract human form, cool color palette, dramatic lighting, sci-fi atmosphere',
      'ethereal scene, light streams, geometric patterns, modern architecture, warm accents, contemplative mood, high detail',
      'dark atmosphere, glowing edges, abstract figure, blue and gold lighting, futuristic, particles floating, cinematic render',
      'emerging light, hope theme, warm tones emerging from dark, abstract human, ethereal, hopeful atmosphere, cinematic'
    ];
    return prompts[index] || prompts[0];
  },

  /**
   * 延迟工具
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },

  /**
   * 获取 Agent 名称
   */
  getAgentName(stageId) {
    const names = {
      topic: '选题 Agent',
      script: '脚本 Agent',
      visual: '画面 Agent',
      generate: '生成 Agent'
    };
    return names[stageId] || stageId;
  },

  /**
   * 获取阶段描述
   */
  getStageDescription(stageId) {
    const descriptions = {
      topic: '从主题生成 5 个选题',
      script: '从选题生成完整脚本',
      visual: '从脚本生成分镜描述',
      generate: '生成图片和视频'
    };
    return descriptions[stageId] || '';
  }
};

// 暴露到全局
window.Agents = Agents;