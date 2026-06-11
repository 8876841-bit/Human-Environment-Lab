/**
 * localStorage 数据存储模块
 */

const STORAGE_KEY = 'hel_agent_studio';

const Store = {
  /**
   * 获取所有数据
   */
  getAll() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : { tasks: [], settings: {} };
    } catch (e) {
      console.error('Store getAll error:', e);
      return { tasks: [], settings: {} };
    }
  },

  /**
   * 保存数据
   */
  save(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      return true;
    } catch (e) {
      console.error('Store save error:', e);
      return false;
    }
  },

  /**
   * 获取所有任务
   */
  getTasks() {
    return this.getAll().tasks;
  },

  /**
   * 获取单个任务
   */
  getTask(id) {
    const tasks = this.getTasks();
    return tasks.find(t => t.id === id);
  },

  /**
   * 创建新任务
   */
  createTask(topic) {
    const data = this.getAll();
    const task = {
      id: Date.now().toString(),
      topic: topic,
      status: 'pending', // pending, running, completed, failed
      currentStage: 0,
      stages: [
        { id: 'topic', name: '选题', status: 'pending', result: null },
        { id: 'script', name: '脚本', status: 'pending', result: null },
        { id: 'visual', name: '画面', status: 'pending', result: null },
        { id: 'generate', name: '生成', status: 'pending', result: null }
      ],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    data.tasks.unshift(task);
    this.save(data);
    return task;
  },

  /**
   * 更新任务
   */
  updateTask(id, updates) {
    const data = this.getAll();
    const index = data.tasks.findIndex(t => t.id === id);
    if (index === -1) return null;

    data.tasks[index] = {
      ...data.tasks[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    this.save(data);
    return data.tasks[index];
  },

  /**
   * 更新任务阶段状态
   */
  updateTaskStage(taskId, stageId, stageData) {
    const data = this.getAll();
    const task = data.tasks.find(t => t.id === taskId);
    if (!task) return null;

    const stageIndex = task.stages.findIndex(s => s.id === stageId);
    if (stageIndex === -1) return null;

    task.stages[stageIndex] = { ...task.stages[stageIndex], ...stageData };
    task.updatedAt = new Date().toISOString();

    // 更新当前阶段
    const nextPendingIndex = task.stages.findIndex(s => s.status === 'pending');
    task.currentStage = nextPendingIndex === -1 ? task.stages.length - 1 : nextPendingIndex - 1;

    // 更新任务状态
    const allDone = task.stages.every(s => s.status === 'done');
    const hasFailed = task.stages.some(s => s.status === 'error');
    if (allDone) task.status = 'completed';
    else if (hasFailed) task.status = 'failed';
    else if (task.stages.some(s => s.status === 'running')) task.status = 'running';

    this.save(data);
    return task;
  },

  /**
   * 删除任务
   */
  deleteTask(id) {
    const data = this.getAll();
    data.tasks = data.tasks.filter(t => t.id !== id);
    this.save(data);
    return true;
  },

  /**
   * 清空所有任务
   */
  clearAll() {
    this.save({ tasks: [], settings: {} });
    return true;
  },

  /**
   * 导出任务为 JSON
   */
  exportTask(id) {
    const task = this.getTask(id);
    if (!task) return null;
    return JSON.stringify(task, null, 2);
  },

  /**
   * 从剪贴板粘贴内容
   */
  async pasteFromClipboard() {
    try {
      return await navigator.clipboard.readText();
    } catch (e) {
      console.error('Clipboard read error:', e);
      return '';
    }
  }
};

// 暴露到全局
window.Store = Store;