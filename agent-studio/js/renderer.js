/**
 * 页面渲染模块
 */

const Renderer = {
  /**
   * 渲染主应用
   */
  renderApp(activeTab = 'workspace') {
    const app = document.getElementById('app');
    if (!app) return;

    app.innerHTML = `
      <nav>
        <div class="wrap">
          <div class="logo">AGENT STUDIO</div>
          <div class="nav-links">
            <a href="#" class="${activeTab === 'workspace' ? 'active' : ''}" data-tab="workspace">工作台</a>
            <a href="#" class="${activeTab === 'history' ? 'active' : ''}" data-tab="history">历史记录</a>
            <a href="#" id="settings-btn">⚙️ API设置</a>
          </div>
        </div>
      </nav>

      <div class="container">
        ${activeTab === 'workspace' ? this.renderWorkspace() : this.renderHistory()}
      </div>
    `;

    // 绑定事件
    this.bindEvents();
  },

  /**
   * 渲染工作台
   */
  renderWorkspace() {
    const tasks = Store.getTasks();
    const activeTask = tasks.find(t => t.status === 'running' || t.status === 'pending') || tasks[0];

    return `
      <h1>多 Agent 内容工作台</h1>
      <p class="subtitle">从选题到生成的完整流水线</p>

      <div class="divider"></div>

      <!-- 新建任务 -->
      <div class="card" style="margin-bottom: 32px;">
        <h3>新建任务</h3>
        <div class="input-group">
          <label>输入主题</label>
          <input type="text" id="topic-input" placeholder="例如：独居人的家、阳台改造、AI与生活...">
        </div>
        <button class="btn btn-primary" id="create-task-btn">
          <span>🚀</span> 创建任务
        </button>
      </div>

      <div class="grid grid-2">
        <!-- 任务列表 -->
        <div>
          <h2>任务队列</h2>
          <div id="task-list" class="task-list">
            ${tasks.length === 0 ? this.renderEmptyTasks() : tasks.map(t => this.renderTaskItem(t)).join('')}
          </div>
        </div>

        <!-- 流程图 + 内容面板 -->
        <div>
          ${activeTask ? this.renderPipeline(activeTask) : this.renderNoTask()}
        </div>
      </div>
    `;
  },

  /**
   * 渲染任务列表项
   */
  renderTaskItem(task) {
    const statusClass = task.status === 'running' ? 'active' : '';
    const time = this.formatTime(task.createdAt);

    return `
      <div class="task-item ${statusClass}" data-task-id="${task.id}">
        <div class="task-header">
          <div>
            <div class="task-title">${this.escapeHtml(task.topic)}</div>
            <div class="task-time">${time}</div>
          </div>
          <div>
            <span class="tag ${task.status === 'completed' ? '' : 'tag-secondary'}">${this.getStatusText(task.status)}</span>
          </div>
        </div>
        <div class="task-progress">
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${this.getProgress(task)}%"></div>
          </div>
        </div>
        <div class="task-stages">
          ${task.stages.map((s, i) => `
            <span class="stage-badge ${s.status === 'done' ? 'done' : i === task.currentStage ? 'active' : ''}">${s.name}</span>
          `).join('')}
        </div>
      </div>
    `;
  },

  /**
   * 渲染空任务状态
   */
  renderEmptyTasks() {
    return `
      <div class="empty-state">
        <div class="icon">📋</div>
        <p>暂无任务</p>
        <p style="font-size: 14px; margin-top: 8px;">输入主题创建第一个任务</p>
      </div>
    `;
  },

  /**
   * 渲染流程图
   */
  renderPipeline(task) {
    return `
      <h2>流水线</h2>
      <div class="pipeline" id="pipeline">
        ${task.stages.map((stage, i) => `
          <div class="pipeline-node ${this.getNodeClass(stage, i, task)}" data-stage="${stage.id}">
            <div class="node-status ${stage.status}">${this.getStatusIcon(stage.status)}</div>
            <div class="node-icon">${this.getStageIcon(stage.id)}</div>
            <div class="node-title">${stage.name}</div>
            <div class="node-desc">${Agents.getStageDescription(stage.id)}</div>
          </div>
          ${i < task.stages.length - 1 ? '<div class="pipeline-arrow">→</div>' : ''}
        `).join('')}
      </div>

      <div class="divider"></div>

      <!-- 内容面板 -->
      <div class="content-panel">
        <div class="content-header">
          <h3 id="panel-title">${task.topic}</h3>
          <div class="actions">
            ${task.status === 'pending' ? `
              <button class="btn btn-primary" id="run-task-btn">
                <span>▶</span> 执行
              </button>
            ` : ''}
            ${task.status === 'running' ? `
              <button class="btn btn-secondary" id="stop-task-btn" disabled>
                <span class="loading-spinner"></span> 执行中...
              </button>
            ` : ''}
            ${task.status === 'completed' ? `
              <button class="btn btn-primary" id="run-task-btn">
                <span>↻</span> 重新执行
              </button>
            ` : ''}
          </div>
        </div>
        <div class="content-body" id="content-body">
          ${this.renderStageContent(task)}
        </div>
      </div>
    `;
  },

  /**
   * 渲染无任务状态
   */
  renderNoTask() {
    return `
      <div class="empty-state">
        <div class="icon">🎬</div>
        <p>选择一个任务开始</p>
        <p style="font-size: 14px; margin-top: 8px;">或者创建一个新任务</p>
      </div>
    `;
  },

  /**
   * 渲染阶段内容
   */
  renderStageContent(task) {
    const currentStage = task.stages[task.currentStage];
    if (!currentStage || !currentStage.result) {
      return `<p style="color: var(--muted);">点击「执行」开始生成内容</p>`;
    }

    return this.formatResult(currentStage.result, currentStage.id);
  },

  /**
   * 格式化结果展示
   */
  formatResult(result, stageId) {
    if (stageId === 'topic') {
      return this.renderTopicResult(result);
    } else if (stageId === 'script') {
      return this.renderScriptResult(result);
    } else if (stageId === 'visual') {
      return this.renderVisualResult(result);
    } else if (stageId === 'generate') {
      return this.renderGenerateResult(result);
    }
    return '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
  },

  /**
   * 渲染选题结果
   */
  renderTopicResult(result) {
    if (!result.topics) return '<p>无内容</p>';
    return `
      <p style="margin-bottom: 16px; color: var(--muted);">生成了 ${result.count} 个选题：</p>
      ${result.topics.map(t => `
        <div class="card" style="margin-bottom: 12px; padding: 16px;">
          <div style="font-weight: 600; color: var(--gold);">${t.id}｜${t.title}</div>
          <div style="margin-top: 8px; font-size: 14px;">${t.description}</div>
          <div style="margin-top: 8px;">
            <span class="stage-badge" style="margin: 2px;">${t.needs.join(', ')}</span>
            <span class="stage-badge" style="margin: 2px;">${t.system}</span>
          </div>
        </div>
      `).join('')}
    `;
  },

  /**
   * 渲染脚本结果
   */
  renderScriptResult(result) {
    const s = result.structure;
    return `
      <div style="margin-bottom: 16px;">
        <span class="tag">${result.duration}</span>
        <span class="tag tag-secondary" style="margin-left: 8px;">${result.style.tone}</span>
      </div>

      <h4 style="color: var(--gold); margin-bottom: 12px;">${s.opening.content}（${s.opening.time}）</h4>
      <p style="font-size: 15px; margin-bottom: 16px; line-height: 1.8;">${s.opening.text}</p>

      <h4 style="color: var(--gold); margin-bottom: 12px;">${s.body1.content}（${s.body1.time}）</h4>
      <p style="font-size: 15px; margin-bottom: 16px; line-height: 1.8;">${s.body1.text}</p>

      <h4 style="color: var(--gold); margin-bottom: 12px;">${s.body2.content}（${s.body2.time}）</h4>
      <p style="font-size: 15px; margin-bottom: 16px; line-height: 1.8;">${s.body2.text}</p>

      <h4 style="color: var(--gold); margin-bottom: 12px;">${s.body3.content}（${s.body3.time}）</h4>
      <p style="font-size: 15px; margin-bottom: 16px; line-height: 1.8;">${s.body3.text}</p>

      <h4 style="color: var(--gold); margin-bottom: 12px;">${s.ending.content}（${s.ending.time}）</h4>
      <p style="font-size: 15px; margin-bottom: 16px; line-height: 1.8;">${s.ending.text}</p>

      <div class="divider"></div>
      <p style="color: var(--muted); font-size: 14px;">🎵 BGM建议：${result.bgm}</p>
    `;
  },

  /**
   * 渲染画面结果
   */
  renderVisualResult(result) {
    return `
      <p style="margin-bottom: 16px; color: var(--muted);">共 ${result.shots.length} 个分镜：</p>
      ${result.shots.map(shot => `
        <div class="card" style="margin-bottom: 16px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 600; color: var(--gold);">分镜 ${shot.index}</span>
            <span class="stage-badge">${shot.time}</span>
          </div>
          <div style="font-size: 14px; margin-bottom: 12px;">${shot.description}</div>

          <div style="background: var(--dark); color: #e8dcc8; padding: 12px; border-radius: 8px; font-size: 13px;">
            <div style="margin-bottom: 8px;"><strong>场景：</strong>${shot.visual.scene}</div>
            <div style="margin-bottom: 8px;"><strong>风格：</strong>${shot.visual.style}</div>
            <div style="margin-bottom: 8px;"><strong>色调：</strong>${shot.visual.color}</div>
            <div style="margin-bottom: 8px;"><strong>氛围：</strong>${shot.visual.atmosphere}</div>
            <div><strong>视角：</strong>${shot.visual.angle}</div>
          </div>

          <div style="margin-top: 12px;">
            <div style="font-size: 12px; color: var(--muted); margin-bottom: 4px;">AI 绘图提示词：</div>
            <code style="font-size: 12px; word-break: break-all;">${shot.prompt}</code>
          </div>
        </div>
      `).join('')}
    `;
  },

  /**
   * 渲染生成结果
   */
  renderGenerateResult(result) {
    let html = '';

    // 显示生成的图片
    if (result.images && result.images.length > 0) {
      html += `<h4 style="margin-bottom: 12px;">🖼️ 生成的图片（${result.images.filter(i => i.status === 'success').length}/${result.images.length}）</h4>`;
      html += `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px;">`;

      for (const img of result.images) {
        if (img.status === 'success') {
          html += `
            <div class="card" style="padding: 12px; text-align: center;">
              <img src="${img.url}" style="width: 100%; border-radius: 8px; margin-bottom: 8px;" alt="生成图片 ${img.shotIndex}">
              <div style="font-size: 12px; color: var(--muted);">分镜 ${img.shotIndex}</div>
            </div>
          `;
        } else {
          html += `
            <div class="card" style="padding: 12px; text-align: center; border-color: var(--danger);">
              <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
              <div style="font-size: 12px; color: var(--danger);">分镜 ${img.shotIndex} 生成失败</div>
              <div style="font-size: 11px; color: var(--muted); margin-top: 4px;">${img.error || '未知错误'}</div>
            </div>
          `;
        }
      }
      html += `</div>`;
    }

    // 显示生成的视频
    if (result.videos && result.videos.length > 0) {
      html += `<h4 style="margin-bottom: 12px;">🎬 生成的视频（${result.videos.filter(v => v.status === 'success').length}/${result.videos.length}）</h4>`;
      html += `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px;">`;

      for (const vid of result.videos) {
        if (vid.status === 'success') {
          html += `
            <div class="card" style="padding: 12px; text-align: center;">
              ${vid.cover_url ? `<img src="${vid.cover_url}" style="width: 100%; border-radius: 8px; margin-bottom: 8px;" alt="视频封面 ${vid.shotIndex}">` : ''}
              <a href="${vid.url}" target="_blank" class="btn btn-primary" style="font-size: 12px; padding: 8px 16px;">下载 分镜 ${vid.shotIndex}</a>
            </div>
          `;
        } else {
          html += `
            <div class="card" style="padding: 12px; text-align: center; border-color: var(--danger);">
              <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
              <div style="font-size: 12px; color: var(--danger);">分镜 ${vid.shotIndex} 视频失败</div>
            </div>
          `;
        }
      }
      html += `</div>`;
    }

    // 如果没有生成任何内容
    if (!result.images || result.images.length === 0) {
      html += `
        <div class="card" style="background: #fff3e0; border-color: #ffcc80; margin-bottom: 16px;">
          <h4 style="color: #e65100; margin-bottom: 8px;">⚡ 等待生成</h4>
          <p style="font-size: 14px;">配置 API Key 后自动生成图片和视频：</p>
          <ul style="margin-top: 12px; font-size: 14px;">
            <li><strong>OpenAI DALL-E 3</strong> - 出图（推荐）</li>
            <li><strong>通义万相</strong> - 出图（备选，免费额度）</li>
            <li><strong>可灵</strong> - 视频生成</li>
          </ul>
          <p style="font-size: 12px; color: var(--muted); margin-top: 12px;">点击右上角 ⚙️ API设置 配置</p>
        </div>
      `;
    }

    // 后续步骤
    html += `<h4 style="margin-bottom: 12px;">📋 后续步骤</h4>`;
    html += result.nextSteps.map((step, i) => `
      <div style="padding: 12px; border-left: 3px solid var(--gold); margin-bottom: 8px; background: var(--card);">
        ${step}
      </div>
    `).join('');

    return html;
  },

  /**
   * 渲染历史记录
   */
  renderHistory() {
    const tasks = Store.getTasks();

    return `
      <h1>历史记录</h1>
      <p class="subtitle">查看已完成的所有任务</p>

      <div class="divider"></div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <span style="color: var(--muted);">共 ${tasks.length} 个任务</span>
        ${tasks.length > 0 ? '<button class="btn btn-danger" id="clear-all-btn">清空全部</button>' : ''}
      </div>

      <div id="history-list">
        ${tasks.length === 0 ? this.renderEmptyHistory() : tasks.map(t => this.renderHistoryItem(t)).join('')}
      </div>
    `;
  },

  /**
   * 渲染历史记录项
   */
  renderHistoryItem(task) {
    const time = this.formatDateTime(task.createdAt);
    const completedStage = task.stages.filter(s => s.status === 'done').length;

    return `
      <div class="history-item">
        <div class="history-info">
          <div class="history-title">${this.escapeHtml(task.topic)}</div>
          <div class="history-meta">
            ${time} · ${completedStage}/${task.stages.length} 阶段完成
          </div>
        </div>
        <div class="history-actions">
          <button class="btn btn-secondary" data-action="view" data-id="${task.id}">查看</button>
          <button class="btn btn-secondary" data-action="export" data-id="${task.id}">导出</button>
          <button class="btn btn-danger" data-action="delete" data-id="${task.id}">删除</button>
        </div>
      </div>
    `;
  },

  /**
   * 渲染空历史
   */
  renderEmptyHistory() {
    return `
      <div class="empty-state">
        <div class="icon">📜</div>
        <p>暂无历史记录</p>
      </div>
    `;
  },

  /**
   * 绑定事件
   */
  bindEvents() {
    // Tab 切换
    document.querySelectorAll('nav a[data-tab]').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = e.target.dataset.tab;
        this.renderApp(tab);
      });
    });

    // 创建任务
    const createBtn = document.getElementById('create-task-btn');
    if (createBtn) {
      createBtn.addEventListener('click', () => App.createTask());
    }

    // 回车创建任务
    const input = document.getElementById('topic-input');
    if (input) {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') App.createTask();
      });
    }

    // 执行任务
    const runBtn = document.getElementById('run-task-btn');
    if (runBtn) {
      runBtn.addEventListener('click', () => App.runCurrentTask());
    }

    // 任务列表点击
    document.querySelectorAll('.task-item').forEach(item => {
      item.addEventListener('click', () => {
        const taskId = item.dataset.taskId;
        App.selectTask(taskId);
      });
    });

    // 清空全部
    const clearBtn = document.getElementById('clear-all-btn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (confirm('确定要清空所有历史记录吗？')) {
          Store.clearAll();
          this.renderApp('history');
          App.showToast('已清空', 'success');
        }
      });
    }

    // 历史操作按钮
    document.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const action = btn.dataset.action;
        const id = btn.dataset.id;
        if (action === 'view') App.selectTask(id, 'workspace');
        else if (action === 'export') App.exportTask(id);
        else if (action === 'delete') App.deleteTask(id);
      });
    });

    // 设置按钮
    const settingsBtn = document.getElementById('settings-btn');
    if (settingsBtn) {
      settingsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        App.openSettings();
      });
    }
  },

  /**
   * 显示设置弹窗
   */
  showSettingsModal() {
    const existingModal = document.querySelector('.modal-overlay');
    if (existingModal) existingModal.remove();

    const keys = Store.getApiKeys();

    const modal = document.createElement('div');
    modal.className = 'modal-overlay active';
    modal.innerHTML = `
      <div class="modal" style="max-width: 500px;">
        <div class="modal-header">
          <h3>API 设置</h3>
          <button class="modal-close" id="close-settings-btn">×</button>
        </div>
        <p style="color: var(--muted); font-size: 14px; margin-bottom: 24px;">
          配置你的 API Keys，所有密钥存储在本地浏览器中，不会上传到任何服务器。
        </p>

        <div class="input-group">
          <label>OpenAI API Key</label>
          <input type="password" id="api-openai" placeholder="sk-..." value="${keys.openai || ''}">
          <small style="color: var(--muted); font-size: 12px; margin-top: 4px; display: block;">
            用于：选题Agent、脚本Agent、DALL-E图片生成
          </small>
        </div>

        <div class="input-group">
          <label>通义万相 API Key（备选）</label>
          <input type="password" id="api-dashscope" placeholder="sk-..." value="${keys.dashscope || ''}">
          <small style="color: var(--muted); font-size: 12px; margin-top: 4px; display: block;">
            用于：出图（免费额度），可替代 OpenAI
          </small>
        </div>

        <div class="input-group">
          <label>可灵 API Key（视频）</label>
          <input type="password" id="api-kling" placeholder="AK...SK..." value="${keys.kling || ''}">
          <small style="color: var(--muted); font-size: 12px; margin-top: 4px; display: block;">
            用于：视频生成 | <a href="https://platform.klingai.com" target="_blank" style="color: var(--gold);">获取Key →</a>
          </small>
        </div>

        <div class="actions" style="margin-top: 24px;">
          <button class="btn btn-primary" id="save-api-btn">💾 保存</button>
          <button class="btn btn-secondary" id="test-api-btn">🔬 测试连接</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // 绑定事件
    document.getElementById('close-settings-btn').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });

    document.getElementById('save-api-btn').addEventListener('click', () => {
      const keys = {
        openai: document.getElementById('api-openai').value.trim(),
        dashscope: document.getElementById('api-dashscope').value.trim(),
        kling: document.getElementById('api-kling').value.trim()
      };
      App.saveApiKeys(keys);
      modal.remove();
    });

    document.getElementById('test-api-btn').addEventListener('click', async () => {
      const openaiKey = document.getElementById('api-openai').value.trim();
      if (openaiKey) {
        try {
          const response = await fetch('https://api.openai.com/v1/models', {
            headers: { 'Authorization': `Bearer ${openaiKey}` }
          });
          if (response.ok) {
            this.showToast('OpenAI API 连接成功！', 'success');
          } else {
            this.showToast('API Key 无效', 'error');
          }
        } catch (e) {
          this.showToast('连接失败：' + e.message, 'error');
        }
      } else {
        this.showToast('请先输入 API Key', 'error');
      }
    });
  },

  /**
   * 显示 Toast 通知
   */
  showToast(message, type = 'info') {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  },

  // ===== 工具方法 =====

  getStageIcon(stageId) {
    const icons = { topic: '💡', script: '📝', visual: '🎨', generate: '🎬' };
    return icons[stageId] || '⚙️';
  },

  getStatusIcon(status) {
    const icons = { pending: '⏳', running: '⚡', done: '✓', error: '✗' };
    return icons[status] || '•';
  },

  getStatusText(status) {
    const texts = { pending: '待处理', running: '执行中', completed: '已完成', failed: '失败' };
    return texts[status] || status;
  },

  getNodeClass(stage, index, task) {
    if (stage.status === 'done') return 'completed';
    if (stage.status === 'error') return 'failed';
    if (index === task.currentStage && stage.status === 'running') return 'active';
    return '';
  },

  getProgress(task) {
    const done = task.stages.filter(s => s.status === 'done').length;
    return Math.round((done / task.stages.length) * 100);
  },

  formatTime(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return Math.floor(diff / 60000) + ' 分钟前';
    if (diff < 86400000) return Math.floor(diff / 3600000) + ' 小时前';
    return date.toLocaleDateString('zh-CN');
  },

  formatDateTime(dateStr) {
    return new Date(dateStr).toLocaleString('zh-CN');
  },

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
};

// 暴露到全局
window.Renderer = Renderer;