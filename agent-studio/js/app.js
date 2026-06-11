/**
 * 主应用逻辑
 */

const App = {
  currentTaskId: null,
  isRunning: false,

  /**
   * 初始化应用
   */
  init() {
    this.render();
  },

  /**
   * 渲染应用
   */
  render() {
    Renderer.renderApp('workspace');
  },

  /**
   * 打开设置弹窗
   */
  openSettings() {
    Renderer.showSettingsModal();
  },

  /**
   * 保存 API Keys
   */
  saveApiKeys(keys) {
    Store.saveApiKeys(keys);
    Renderer.showToast('API Keys 已保存', 'success');
  },

  /**
   * 检查 API Key 是否已配置
   */
  hasApiKey(name) {
    const key = Store.getApiKey(name);
    return key && key.length > 0;
  },

  /**
   * 获取 API Key
   */
  getApiKey(name) {
    return Store.getApiKey(name);
  },

  /**
   * 创建新任务
   */
  createTask() {
    const input = document.getElementById('topic-input');
    const topic = input?.value.trim();

    if (!topic) {
      Renderer.showToast('请输入主题', 'error');
      input?.focus();
      return;
    }

    const task = Store.createTask(topic);
    this.currentTaskId = task.id;
    this.render();
    Renderer.showToast('任务已创建', 'success');

    // 滚动到任务列表顶部
    document.querySelector('.task-list')?.scrollIntoView({ behavior: 'smooth' });
  },

  /**
   * 选择任务
   */
  selectTask(taskId, tab = null) {
    this.currentTaskId = taskId;
    if (tab) {
      Renderer.renderApp(tab);
    } else {
      this.render();
    }
  },

  /**
   * 执行当前任务
   */
  async runCurrentTask() {
    if (this.isRunning) return;

    // 获取当前任务
    const task = this.currentTaskId
      ? Store.getTask(this.currentTaskId)
      : Store.getTasks()[0];

    if (!task) {
      Renderer.showToast('没有可执行的任务', 'error');
      return;
    }

    this.currentTaskId = task.id;
    this.isRunning = true;

    // 更新任务状态
    Store.updateTask(task.id, { status: 'running' });
    this.render();

    // 依次执行各阶段
    const stages = [
      { id: 'topic', agent: 'topicAgent', input: task.topic },
      { id: 'script', agent: 'scriptAgent', inputKey: 'topic' },
      { id: 'visual', agent: 'visualAgent', inputKey: 'script' },
      { id: 'generate', agent: 'generateAgent', inputKey: 'visual' }
    ];

    for (const stage of stages) {
      if (!this.isRunning) break;

      // 更新阶段状态为运行中
      Store.updateTaskStage(task.id, stage.id, { status: 'running', result: null });
      this.render();

      try {
        // 获取输入
        let input;
        if (stage.input !== undefined) {
          input = stage.input;
        } else if (stage.inputKey) {
          const currentStageIndex = stages.findIndex(s => s.id === stage.id);
          const prevStage = stages[currentStageIndex - 1];
          const taskData = Store.getTask(task.id);
          const prevResult = taskData.stages.find(s => s.id === prevStage.id)?.result;
          input = prevResult;
        }

        // 调用 Agent
        const agentMethod = stage.agent;
        const result = await Agents[agentMethod](input);

        // 更新阶段结果
        Store.updateTaskStage(task.id, stage.id, { status: 'done', result });
        this.render();

      } catch (error) {
        console.error(`Stage ${stage.id} error:`, error);
        Store.updateTaskStage(task.id, stage.id, { status: 'error', result: { error: error.message } });
        this.render();
        Renderer.showToast(`${stage.id} 阶段执行失败`, 'error');
        break;
      }
    }

    // 更新最终状态
    const finalTask = Store.getTask(task.id);
    if (finalTask) {
      const allDone = finalTask.stages.every(s => s.status === 'done');
      Store.updateTask(task.id, { status: allDone ? 'completed' : 'failed' });
    }

    this.isRunning = false;
    this.render();

    if (allDone) {
      Renderer.showToast('任务完成！', 'success');
    }
  },

  /**
   * 导出任务
   */
  exportTask(taskId) {
    const json = Store.exportTask(taskId);
    if (!json) {
      Renderer.showToast('导出失败', 'error');
      return;
    }

    // 创建下载
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `task_${taskId}.json`;
    a.click();
    URL.revokeObjectURL(url);

    Renderer.showToast('已导出', 'success');
  },

  /**
   * 删除任务
   */
  deleteTask(taskId) {
    if (confirm('确定删除这个任务？')) {
      Store.deleteTask(taskId);
      if (this.currentTaskId === taskId) {
        this.currentTaskId = null;
      }
      Renderer.renderApp('history');
      Renderer.showToast('已删除', 'success');
    }
  },

  /**
   * 显示 Toast
   */
  showToast(message, type = 'info') {
    Renderer.showToast(message, type);
  }
};

// 暴露到全局
window.App = App;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => App.init());