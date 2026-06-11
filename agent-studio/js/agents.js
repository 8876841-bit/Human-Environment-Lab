/**
 * 各 Agent 模拟逻辑
 * 模拟真实场景下的内容生成过程
 */

const Agents = {
  /**
   * 选题 Agent - 生成 30 个选题
   */
  async topicAgent(topic) {
    // 模拟网络延迟
    await this.delay(1500 + Math.random() * 1000);

    const topics = [
      '独居人的厨房收纳哲学',
      '阳台绿植与城市焦虑',
      '出租屋改造：家的边界感',
      '智能音箱与家庭对话消失',
      '咖啡角：都市人的精神角落',
      '玄关的仪式感：从疲惫到放松',
      '书桌与生产力幻觉',
      '衣柜里的四季人生',
      '浴室：一个私密王国的崩塌',
      '客厅沙发与家庭权力结构'
    ];

    const selected = topics.slice(0, 5).map((t, i) => ({
      id: `OBS-${String(i + 1).padStart(3, '0')}`,
      title: t,
      description: `${t}：探讨人在这个空间里的真实需求和行为模式`,
      needs: ['效率', '掌控', '连接'],
      behavior: ['放', '拿', '找'],
      environment: ['光', '材料', '空间'],
      system: '家庭系统'
    }));

    return {
      count: 5,
      topics: selected,
      timestamp: new Date().toISOString()
    };
  },

  /**
   * 脚本 Agent - 生成 1 分钟视频脚本
   */
  async scriptAgent(topicResult) {
    await this.delay(2000 + Math.random() * 1500);

    const selectedTopic = topicResult.topics[0];
    const script = {
      title: selectedTopic.title,
      duration: '60秒',
      structure: {
        opening: {
          time: '0-5秒',
          content: '钩子：让人停下来的一句话',
          text: `你有没有想过，为什么同样是回家，有些人的家会让他们放松，有些人的家反而更累？`
        },
        body1: {
          time: '5-20秒',
          content: '提出问题或现象',
          text: `我们花了很多时间研究装修风格、板材选择、五金配置。但很少有人问：${selectedTopic.title}这件事，到底在解决什么问题？`
        },
        body2: {
          time: '20-40秒',
          content: '深入分析或故事',
          text: `我观察了很多家庭，发现一个规律：当空间设计真正从"人怎么生活"出发，而不是从"好看不好看"出发的时候，那个空间会自己说话。它会让人自动进入某种状态——或者放松，或者专注，或者连接。`
        },
        body3: {
          time: '40-55秒',
          content: '核心观点',
          text: `${selectedTopic.description.split('：')[0]}，本质上是在回答一个问题：人需要什么样的环境才能成为更好的自己？`
        },
        ending: {
          time: '55-60秒',
          content: '留白或引发思考的问题',
          text: `所以，下次当你站在自己的空间里，问自己一个问题：这个环境，是让我更像我自己，还是正在把我变成别人期待的样子？`
        }
      },
      style: {
        tone: '轻盈、有深度、有见解',
        pace: '适中，留白感',
        forbidden: ['AI腔', '套话', '说教', '夸张语气']
      },
      bgm: '建议：Ambient、Lo-fi、或简约钢琴曲',
      timestamp: new Date().toISOString()
    };

    return script;
  },

  /**
   * 画面 Agent - 生成分镜描述
   */
  async visualAgent(scriptResult) {
    await this.delay(1500 + Math.random() * 1000);

    const story = scriptResult.structure;
    const storyParts = [story.opening, story.body1, story.body2, story.body3, story.ending];

    const shots = storyParts.map((part, i) => ({
      index: i + 1,
      time: part.time,
      description: part.content,
      visual: {
        scene: this.generateScene(i, part.content),
        subject: '抽象概念化的人物轮廓',
        style: '抽象艺术 + 科幻感 + 未来感',
        color: i % 2 === 0 ? '深蓝/深灰背景' : '暖色点缀',
        atmosphere: i < 2 ? '沉稳' : '渐入希望',
        angle: ['主观视角', '俯拍', '特写', '全景', '仰拍'][i]
      },
      prompt: this.generatePrompt(i, part),
      motion: i < 2 ? '缓慢' : '流动'
    }));

    return {
      title: scriptResult.title,
      shots: shots,
      styleGuide: {
        overall: '抽象艺术 + 科幻感 + 未来感 + 代入感',
        avoid: '写实主义、过于具象',
        colorPalette: '深色系为主（深蓝/深灰/黑色背景），点缀色（金色/蓝色/白色光线）',
        effects: ['粒子效果', '几何图形', '光线流动']
      },
      timestamp: new Date().toISOString()
    };
  },

  /**
   * 生成 Agent - 生成图片/视频（目前是占位）
   */
  async generateAgent(visualResult) {
    await this.delay(2500 + Math.random() * 1500);

    const assets = visualResult.shots.map((shot, i) => ({
      shotIndex: i + 1,
      image: {
        status: 'ready',
        path: `generated/images/${visualResult.title}_shot_${i + 1}.png`,
        note: '需要接入 Liblib API 生成'
      },
      video: {
        status: 'ready',
        path: `generated/videos/${visualResult.title}_shot_${i + 1}.mp4`,
        duration: '5-10秒',
        note: '需要接入 TapNow API 生成'
      }
    }));

    return {
      title: visualResult.title,
      assets: assets,
      status: 'ready_for_review',
      nextSteps: [
        '1. 查看生成的图片（需接入 Liblib）',
        '2. 查看生成的视频（需接入 TapNow）',
        '3. 用剪映拼接成完整视频',
        '4. 添加 BGM 和字幕',
        '5. 发布'
      ],
      timestamp: new Date().toISOString()
    };
  },

  /**
   * 生成场景描述
   */
  generateScene(index, content) {
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
  generatePrompt(index, part) {
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