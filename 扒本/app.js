/**
 * ScriptGenius AI - Video Batch to Screenplay App
 * Engine: Python Native SSE Stream Engine
 */

const PROMPT_PRESETS = {
  cn: `你是一位资深影视拉片师与专业短剧编剧。请根据我提供的视频素材，严格按照以下【高遵从度短剧拉片统一规范】，将画面和台词 1:1 精准还原为专业剧本。

========================================
【最高控制禁令（违者整篇作废）】
========================================
1. 【一个场景默认仅写 1 条主▲】：
   - 同一物理场景开局只写 1 条主▲（交代人物初始位置与核心环境）。
   - 连续对话过程中绝对禁止因为镜头视角切换（如近景/特写/切角）而新建▲！同一场景内全篇保持单▲统领台词！仅当有新人物推门入画或重大物理换场时才允许新建▲！
2. 【绝对禁止重复描写UI/系统面板】：
   - 画面中悬浮的系统界面/粉色面板/蓝色面板等视觉元素，全剧仅在首条▲中提及一次！
   - 后续所有▲和台词中，绝对严禁再次出现“面前浮现面板/悬浮界面/心形图案”等任何重复字眼！
3. 【彻底跳过无信息量微动作】：
   - 严禁描写“端起茶杯、喝了一口、放下茶杯、抬手看手、坐下、站起”等日常过渡微动作！仅保留推动剧情冲突的绝对核心动作。

========================================
【基础格式规范】
========================================
第X集
X-1、场景名 日/夜 内/外
人物：本场所有出场人物（按出场顺序排列）

▲ 环境描写+人物初始位置与核心冲突动作（全场默认仅此一条▲，后续对话严禁插入新的▲）。
人物（情绪）：台词内容。
系统（VO）：画外音/系统提示音。
人物（OS）：内心独白。

========================================
【台词与情绪规范】
========================================
1. 【台词 1:1 绝对还原】：逐字逐句保留所有台词与口语语气词，绝对禁止概括或省略！同一人物连续的一段台词必须合并为一句，严禁拆分成多行！
2. 【情绪词绝不重复】：同一人物全剧中，同一情绪词不得出现超过 2 次！严禁一律使用“震惊/崩溃”！
   - 优先匹配具象神态词：怔住、错愕、苦笑、冷笑、恼怒、不解、做贼心虚、难以置信、目瞪口呆。
   - 平静中性台词直接省略括号或标（平静），严禁强行归类到极限情绪！
3. 【用词禁令】：严禁使用“眸光、眼帘、神色一滞、颓然、心绪”等不可拍摄的文学虚词！全程禁止出现任何英文或思考过程！`,

  overseas: `你是一位资深影视拉片师与专业编剧。请根据我按时间轴顺序提供的海外视频高密度切片，将画面和台词 1:1 还原为双语剧本。`
};

const state = {
  currentTheme: localStorage.getItem('scriptgenius_theme') || 'light',
  currentPresetKey: 'cn',
  customPrompts: {
    cn: PROMPT_PRESETS.cn,
    overseas: PROMPT_PRESETS.overseas
  },
  apiConfig: {
    apiKey: localStorage.getItem('scriptgenius_api_key') || '',
    baseUrl: localStorage.getItem('scriptgenius_base_url') || '',
    modelName: localStorage.getItem('scriptgenius_model_name') || 'qwen-vl-max',
    protocol: localStorage.getItem('scriptgenius_protocol') || 'openai',
    concurrency: parseInt(localStorage.getItem('scriptgenius_concurrency') || '2', 10)
  },
  files: [],
  activeFileId: null,
  isQueueRunning: false,
  activeConcurrencies: 0
};

const DOM = {
  themeSelect: document.getElementById('theme-select'),
  presetTrack: document.getElementById('preset-track'),
  btnPresetCn: document.getElementById('btn-preset-cn'),
  btnPresetOverseas: document.getElementById('btn-preset-overseas'),
  currentPresetLabel: document.getElementById('current-preset-label'),
  btnViewPrompt: document.getElementById('btn-view-prompt'),

  dropzone: document.getElementById('dropzone'),
  fileInput: document.getElementById('file-input'),
  fileQueueList: document.getElementById('file-queue-list'),
  emptyState: document.getElementById('empty-state'),
  fileCountBadge: document.getElementById('file-count-badge'),
  
  btnStartQueue: document.getElementById('btn-start-queue'),
  btnPauseQueue: document.getElementById('btn-pause-queue'),
  btnClearQueue: document.getElementById('btn-clear-queue'),
  overallProgressBox: document.getElementById('overall-progress-box'),
  queueStatusText: document.getElementById('queue-status-text'),
  queuePercentage: document.getElementById('queue-percentage'),
  queueProgressBar: document.getElementById('queue-progress-bar'),

  activeFileTitle: document.getElementById('active-file-title'),
  activeFileStatus: document.getElementById('active-file-status'),
  scriptTextarea: document.getElementById('script-textarea'),
  formattedPreviewBox: document.getElementById('formatted-preview-box'),
  charCount: document.getElementById('char-count'),
  sceneCount: document.getElementById('scene-count'),
  modelUsedInfo: document.getElementById('model-used-info'),
  footerMsg: document.getElementById('footer-msg'),
  
  btnSaveFile: document.getElementById('btn-save-file'),
  saveFileDropdown: document.getElementById('save-file-dropdown'),
  btnBatchExport: document.getElementById('btn-batch-export'),
  btnReanalyze: document.getElementById('btn-reanalyze'),
  
  tabBtnEditor: document.getElementById('tab-btn-editor'),
  tabBtnPreview: document.getElementById('tab-btn-preview'),
  tabContentEditor: document.getElementById('tab-content-editor'),
  tabContentPreview: document.getElementById('tab-content-preview'),

  btnApiConfig: document.getElementById('btn-api-config'),
  apiStatusDot: document.getElementById('api-status-dot'),
  apiModal: document.getElementById('api-modal'),
  btnCloseApiModal: document.getElementById('btn-close-api-modal'),
  apiKeyInput: document.getElementById('api-key-input'),
  baseUrlInput: document.getElementById('base-url-input'),
  modelNameInput: document.getElementById('model-name-input'),
  btnFetchModels: document.getElementById('btn-fetch-models'),
  modelsDatalist: document.getElementById('models-datalist'),
  fetchedModelsWrapper: document.getElementById('fetched-models-wrapper'),
  fetchedModelsSelect: document.getElementById('fetched-models-select'),
  apiProtocolSelect: document.getElementById('api-protocol-select'),
  concurrencySelect: document.getElementById('concurrency-select'),
  btnToggleKeyVisibility: document.getElementById('btn-toggle-key-visibility'),
  btnTestApi: document.getElementById('btn-test-api'),
  btnSaveApi: document.getElementById('btn-save-api'),

  promptModal: document.getElementById('prompt-modal'),
  btnClosePromptModal: document.getElementById('btn-close-prompt-modal'),
  promptModalTextarea: document.getElementById('prompt-modal-textarea'),
  btnResetPrompt: document.getElementById('btn-reset-prompt'),
  btnApplyPrompt: document.getElementById('btn-apply-prompt'),

  toastContainer: document.getElementById('toast-container')
};

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initApiModalValues();
  setupEventListeners();
  updateApiStatusIndicator();
  updateModelInfoFooter();
});

function initTheme() {
  if (DOM.themeSelect) {
    DOM.themeSelect.value = state.currentTheme;
    document.body.setAttribute('data-theme', state.currentTheme);
  }
}

function initApiModalValues() {
  DOM.apiKeyInput.value = state.apiConfig.apiKey;
  DOM.baseUrlInput.value = state.apiConfig.baseUrl;
  DOM.modelNameInput.value = state.apiConfig.modelName;
  DOM.apiProtocolSelect.value = state.apiConfig.protocol;
  DOM.concurrencySelect.value = state.apiConfig.concurrency;
}

function updateApiStatusIndicator() {
  if (state.apiConfig.apiKey && state.apiConfig.baseUrl) {
    DOM.apiStatusDot.classList.add('configured');
  } else {
    DOM.apiStatusDot.classList.remove('configured');
  }
}

function updateModelInfoFooter() {
  DOM.modelUsedInfo.innerHTML = `<i class="fa-solid fa-robot"></i> 模型：${state.apiConfig.modelName}`;
}

function setupEventListeners() {
  DOM.themeSelect.addEventListener('change', (e) => {
    state.currentTheme = e.target.value;
    document.body.setAttribute('data-theme', state.currentTheme);
    localStorage.setItem('scriptgenius_theme', state.currentTheme);
  });

  DOM.btnPresetCn.addEventListener('click', () => switchPreset('cn'));
  DOM.btnPresetOverseas.addEventListener('click', () => switchPreset('overseas'));

  DOM.btnViewPrompt.addEventListener('click', openPromptModal);
  DOM.btnClosePromptModal.addEventListener('click', closePromptModal);
  DOM.btnResetPrompt.addEventListener('click', resetPromptToDefault);
  DOM.btnApplyPrompt.addEventListener('click', applyCustomPrompt);

  DOM.dropzone.addEventListener('click', () => DOM.fileInput.click());
  DOM.fileInput.addEventListener('change', (e) => handleFilesAdded(e.target.files));

  DOM.btnStartQueue.addEventListener('click', startQueueProcessing);
  DOM.btnPauseQueue.addEventListener('click', pauseQueueProcessing);
  DOM.btnClearQueue.addEventListener('click', clearQueue);

  DOM.scriptTextarea.addEventListener('input', handleEditorInput);

  DOM.tabBtnEditor.addEventListener('click', () => switchTab('editor'));
  DOM.tabBtnPreview.addEventListener('click', () => switchTab('preview'));

  DOM.btnApiConfig.addEventListener('click', openApiModal);
  DOM.btnCloseApiModal.addEventListener('click', closeApiModal);
  DOM.btnSaveApi.addEventListener('click', saveApiConfig);
  DOM.btnTestApi.addEventListener('click', testApiConnection);
  
  DOM.btnFetchModels.addEventListener('click', fetchModelsList);
  DOM.fetchedModelsSelect.addEventListener('change', (e) => {
    if (e.target.value) {
      DOM.modelNameInput.value = e.target.value;
    }
  });

  DOM.btnToggleKeyVisibility.addEventListener('click', () => {
    const isPass = DOM.apiKeyInput.type === 'password';
    DOM.apiKeyInput.type = isPass ? 'text' : 'password';
    DOM.btnToggleKeyVisibility.innerHTML = `<i class="fa-solid fa-eye${isPass ? '-slash' : ''}"></i>`;
  });
}

function switchPreset(key) {
  state.currentPresetKey = key;
  if (key === 'overseas') {
    DOM.presetTrack.classList.add('overseas');
    DOM.btnPresetCn.classList.remove('active');
    DOM.btnPresetOverseas.classList.add('active');
    DOM.currentPresetLabel.innerHTML = `<i class="fa-solid fa-check"></i> 当前：海外中英双语剧本模式`;
  } else {
    DOM.presetTrack.classList.remove('overseas');
    DOM.btnPresetOverseas.classList.remove('active');
    DOM.btnPresetCn.classList.add('active');
    DOM.currentPresetLabel.innerHTML = `<i class="fa-solid fa-check"></i> 当前：中文国内剧本模式`;
  }
}

function openPromptModal() {
  DOM.promptModalTextarea.value = state.customPrompts[state.currentPresetKey];
  DOM.promptModal.classList.add('show');
}
function closePromptModal() {
  DOM.promptModal.classList.remove('show');
}
function resetPromptToDefault() {
  state.customPrompts[state.currentPresetKey] = PROMPT_PRESETS[state.currentPresetKey];
  DOM.promptModalTextarea.value = state.customPrompts[state.currentPresetKey];
  showToast('提示词已重置为系统默认规则', 'success');
}
function applyCustomPrompt() {
  state.customPrompts[state.currentPresetKey] = DOM.promptModalTextarea.value;
  closePromptModal();
  showToast('已保存自定义提示词', 'success');
}

function handleFilesAdded(fileList) {
  if (!fileList || fileList.length === 0) return;

  let addedCount = 0;
  Array.from(fileList).forEach(file => {
    if (file.type.startsWith('video/') || isVideoExtension(file.name)) {
      const fileObj = {
        id: 'file_' + Math.random().toString(36).substring(2, 9),
        file: file,
        name: file.name,
        size: formatFileSize(file.size),
        status: 'pending',
        script: '',
        errorMsg: ''
      };
      state.files.push(fileObj);
      addedCount++;
    }
  });

  if (addedCount > 0) {
    showToast(`成功导入 ${addedCount} 个视频文件`, 'success');
    renderQueueList();
    updateQueueStats();
    
    if (!state.activeFileId && state.files.length > 0) {
      selectActiveFile(state.files[0].id);
    }
  }

  DOM.fileInput.value = '';
}

function isVideoExtension(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  return ['mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp'].includes(ext);
}

function renderQueueList() {
  if (state.files.length === 0) {
    DOM.emptyState.style.display = 'flex';
    DOM.fileQueueList.innerHTML = '';
    DOM.fileQueueList.appendChild(DOM.emptyState);
    return;
  }

  DOM.emptyState.style.display = 'none';
  DOM.fileQueueList.innerHTML = '';

  state.files.forEach(fileObj => {
    const row = document.createElement('div');
    row.className = `file-item-row ${state.activeFileId === fileObj.id ? 'active' : ''}`;
    row.onclick = () => selectActiveFile(fileObj.id);

    let statusBadgeHtml = '';
    switch (fileObj.status) {
      case 'pending':
        statusBadgeHtml = `<span class="status-badge pending">等待中</span>`;
        break;
      case 'processing':
        statusBadgeHtml = `<span class="status-badge processing"><i class="fa-solid fa-spinner fa-spin"></i> 分析中</span>`;
        break;
      case 'completed':
        statusBadgeHtml = `<span class="status-badge completed"><i class="fa-solid fa-check"></i> 完成</span>`;
        break;
      case 'error':
        statusBadgeHtml = `<span class="status-badge error" title="${escapeHtml(fileObj.errorMsg || '')}"><i class="fa-solid fa-triangle-exclamation"></i> 失败</span>`;
        break;
    }

    row.innerHTML = `
      <div class="file-name-cell" title="${escapeHtml(fileObj.name)}">
        <i class="fa-solid fa-file-video"></i>
        <span>${escapeHtml(fileObj.name)}</span>
      </div>
      <div class="file-size-cell">${fileObj.size}</div>
      <div>${statusBadgeHtml}</div>
      <div>
        <button class="btn-remove-file" title="移除此文件" onclick="event.stopPropagation(); removeFile('${fileObj.id}')">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    `;

    DOM.fileQueueList.appendChild(row);
  });
}

function selectActiveFile(id) {
  state.activeFileId = id;
  const fileObj = state.files.find(f => f.id === id);
  if (!fileObj) return;

  DOM.activeFileTitle.innerText = fileObj.name;
  
  if (fileObj.status === 'error') {
    DOM.scriptTextarea.value = `❌ 【分析失败】文件：${fileObj.name}\n\n原因：${fileObj.errorMsg}\n\n【排查提示】：请在右上角【API 接口设置】中填入有效 Base URL、Key 并选择支持视觉分析的模型（如 qwen-vl-max / gpt-4o）。`;
  } else {
    DOM.scriptTextarea.value = fileObj.script || '';
  }
  
  DOM.activeFileStatus.className = `status-pill ${fileObj.status}`;
  DOM.activeFileStatus.innerText = fileObj.status === 'completed' ? '已完成' : 
                                   fileObj.status === 'processing' ? '分析中' : 
                                   fileObj.status === 'error' ? '分析失败' : '等待中';

  renderQueueList();
  handleEditorInput();
}

function removeFile(id) {
  state.files = state.files.filter(f => f.id !== id);
  if (state.activeFileId === id) {
    state.activeFileId = state.files.length > 0 ? state.files[0].id : null;
    if (state.activeFileId) {
      selectActiveFile(state.activeFileId);
    } else {
      DOM.activeFileTitle.innerText = '选择文件预览生成结果';
      DOM.scriptTextarea.value = '';
      handleEditorInput();
    }
  }
  renderQueueList();
  updateQueueStats();
}

function clearQueue() {
  if (state.isQueueRunning) {
    showToast('请先暂停或停止正在运行的队列', 'error');
    return;
  }
  state.files = [];
  state.activeFileId = null;
  DOM.activeFileTitle.innerText = '选择文件预览生成结果';
  DOM.scriptTextarea.value = '';
  renderQueueList();
  updateQueueStats();
  handleEditorInput();
  showToast('队列列表已清空', 'info');
}

function updateQueueStats() {
  const total = state.files.length;
  DOM.fileCountBadge.innerText = `${total} 个文件`;
  DOM.btnStartQueue.disabled = total === 0;

  const completed = state.files.filter(f => f.status === 'completed').length;
  const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

  if (total > 0 && state.isQueueRunning) {
    DOM.overallProgressBox.style.display = 'block';
    DOM.queueStatusText.innerText = `处理进度: ${completed} / ${total}`;
    DOM.queuePercentage.innerText = `${percent}%`;
    DOM.queueProgressBar.style.width = `${percent}%`;
  } else if (!state.isQueueRunning) {
    DOM.overallProgressBox.style.display = 'none';
  }
}

function startQueueProcessing() {
  const currentKey = DOM.apiKeyInput.value.trim() || state.apiConfig.apiKey;
  const currentBaseUrl = DOM.baseUrlInput.value.trim() || state.apiConfig.baseUrl;

  if (!currentKey || !currentBaseUrl) {
    openApiModal();
    showToast('请先在右上角【API 接口设置】中填入新网站的 Base URL 和 API Key！', 'error');
    return;
  }

  state.apiConfig.apiKey = currentKey;
  state.apiConfig.baseUrl = currentBaseUrl;

  state.files.forEach(f => {
    f.status = 'pending';
    f.script = '';
  });
  renderQueueList();

  state.isQueueRunning = true;
  DOM.btnStartQueue.style.display = 'none';
  DOM.btnPauseQueue.style.display = 'inline-flex';
  updateQueueStats();
  
  processNextInQueue();
}

function pauseQueueProcessing() {
  state.isQueueRunning = false;
  DOM.btnStartQueue.style.display = 'inline-flex';
  DOM.btnPauseQueue.style.display = 'none';
  showToast('队列已暂停', 'info');
}

async function processNextInQueue() {
  if (!state.isQueueRunning) return;

  const availableSlots = state.apiConfig.concurrency - state.activeConcurrencies;
  if (availableSlots <= 0) return;

  const nextFiles = state.files.filter(f => f.status === 'pending').slice(0, availableSlots);

  if (nextFiles.length === 0) {
    if (state.activeConcurrencies === 0) {
      state.isQueueRunning = false;
      DOM.btnStartQueue.style.display = 'inline-flex';
      DOM.btnPauseQueue.style.display = 'none';

      const failedCount = state.files.filter(f => f.status === 'error').length;
      const completedCount = state.files.filter(f => f.status === 'completed').length;

      if (failedCount > 0) {
        showToast(`⚠️ 队列分析结束：${completedCount} 个成功，${failedCount} 个文件失败`, 'error');
      } else {
        showToast(`🎉 全部 ${completedCount} 个视频剧本提取任务已顺利完成！`, 'success');
      }
    }
    return;
  }

  nextFiles.forEach(fileObj => {
    state.activeConcurrencies++;
    fileObj.status = 'processing';
    renderQueueList();
    if (state.activeFileId === fileObj.id) selectActiveFile(fileObj.id);

    analyzeVideoFile(fileObj)
      .then(scriptText => {
        if (!scriptText || !scriptText.trim()) {
          throw new Error('API 接口未返回剧本文本内容。');
        }
        fileObj.status = 'completed';
        fileObj.script = scriptText;
        if (state.activeFileId === fileObj.id) selectActiveFile(fileObj.id);
      })
      .catch(err => {
        fileObj.status = 'error';
        fileObj.errorMsg = err.message || 'API 请求异常';
        showToast(`[${fileObj.name}] 分析失败: ${fileObj.errorMsg}`, 'error');
        if (state.activeFileId === fileObj.id) selectActiveFile(fileObj.id);
      })
      .finally(() => {
        state.activeConcurrencies--;
        updateQueueStats();
        renderQueueList();
        processNextInQueue();
      });
  });
}

async function analyzeVideoFile(fileObj) {
  const promptText = state.customPrompts[state.currentPresetKey];
  const liveBaseUrl = (DOM.baseUrlInput.value.trim() || state.apiConfig.baseUrl).replace(/\/+$/, '');
  const liveApiKey = DOM.apiKeyInput.value.trim() || state.apiConfig.apiKey;
  const model = DOM.modelNameInput.value.trim() || state.apiConfig.modelName || 'qwen-vl-max';

  if (!liveBaseUrl || !liveApiKey) {
    throw new Error('未设置 API 地址或 Key，请在右上角【API 接口设置】中配置新站点');
  }

  if (!fileObj.file || !(fileObj.file instanceof Blob)) {
    throw new Error('未获取到有效的视频文件对象，请重新选择视频上传！');
  }

  if (state.activeFileId === fileObj.id) {
    DOM.scriptTextarea.value = '';
    handleEditorInput();
  }

  showToast(`正在传输视频数据并开启 1:1 剧本提取... [${fileObj.name}]`, 'info');

  const formData = new FormData();
  formData.append('video', fileObj.file, fileObj.name || 'video.mp4');
  formData.append('token', getToken());
  formData.append('api_key', liveApiKey);
  formData.append('base_url', liveBaseUrl);
  formData.append('model', model);
  formData.append('prompt', promptText);
  formData.append('no_slice', 'true');
  formData.append('episode_num', '1');

  const response = await fetch('/api/upload_and_analyze', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error(`Python 服务器错误: HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let streamBuffer = '';
  let accumulatedScript = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    streamBuffer += decoder.decode(value, { stream: true });
    const lines = streamBuffer.split('\n\n');
    streamBuffer = lines.pop() || '';

    for (const block of lines) {
      const trimmed = block.trim();
      if (trimmed.startsWith('data: ')) {
        try {
          const data = JSON.parse(trimmed.substring(6));
          if (data.type === 'progress') {
            showToast(data.msg, 'info');
          } else if (data.type === 'chunk') {
            accumulatedScript += (accumulatedScript ? '\n\n' : '') + data.content;
            fileObj.script = accumulatedScript;
            if (state.activeFileId === fileObj.id) {
              DOM.scriptTextarea.value = accumulatedScript;
              DOM.scriptTextarea.scrollTop = DOM.scriptTextarea.scrollHeight;
              handleEditorInput();
            }
            showToast(`已实时完成第 ${data.chunk_index}/${data.total_chunks} 单元打字输出！`, 'success');
          } else if (data.type === 'error') {
            showToast(data.message, 'error');
            throw new Error(data.message);
          } else if (data.type === 'done') {
            showToast(`🎉 1:1 全量剧本拆本提取完成！剧本已直接写入您的电脑桌面！`, 'success');
            return data.full_script || accumulatedScript;
          }
        } catch (e) {
          if (e.message && !e.message.includes('JSON')) throw e;
        }
      }
    }
  }

  if (accumulatedScript) return accumulatedScript;
  throw new Error('模型未返回有效文本内容');
}

function handleEditorInput() {
  const content = DOM.scriptTextarea.value;
  
  if (state.activeFileId) {
    const fileObj = state.files.find(f => f.id === state.activeFileId);
    if (fileObj) fileObj.script = content;
  }

  DOM.charCount.innerText = content.length;
  const scenes = content.match(/\d+-\d+|\d+场/g);
  DOM.sceneCount.innerText = scenes ? scenes.length : (content.length > 0 ? 1 : 0);

  renderFormattedPreview(content);
}

function renderFormattedPreview(text) {
  if (!text || text.trim() === '') {
    DOM.formattedPreviewBox.innerHTML = `
      <div class="placeholder-preview">
        <i class="fa-solid fa-clapperboard"></i>
        <p>在此处查看排版优雅、高亮醒目的专业剧本效果</p>
      </div>
    `;
    return;
  }

  const lines = text.split('\n');
  let html = '';

  lines.forEach(line => {
    const trimmed = line.trim();
    if (!trimmed) {
      html += '<br>';
      return;
    }

    if (trimmed.startsWith('第') && trimmed.includes('集')) {
      html += `<div class="script-episode">${escapeHtml(trimmed)}</div>`;
    } else if (/^\d+-\d+/.test(trimmed)) {
      html += `<div class="script-scene">${escapeHtml(trimmed)}</div>`;
    } else if (trimmed.startsWith('▲')) {
      html += `<div class="script-action">${escapeHtml(trimmed)}</div>`;
    } else if (trimmed.includes('：') || trimmed.includes(':')) {
      const parts = trimmed.split(/：|:/);
      const speaker = parts[0];
      const dialogue = parts.slice(1).join('：');
      html += `<div class="script-action"><span class="script-dialogue-speaker">${escapeHtml(speaker)}：</span>${escapeHtml(dialogue)}</div>`;
    } else {
      html += `<div class="script-action">${escapeHtml(trimmed)}</div>`;
    }
  });

  DOM.formattedPreviewBox.innerHTML = html;
}

function switchTab(tabKey) {
  if (tabKey === 'editor') {
    DOM.tabBtnEditor.classList.add('active');
    DOM.tabBtnPreview.classList.remove('active');
    DOM.tabContentEditor.classList.add('active');
    DOM.tabContentPreview.classList.remove('active');
  } else {
    DOM.tabBtnPreview.classList.add('active');
    DOM.tabBtnEditor.classList.remove('active');
    DOM.tabContentPreview.classList.add('active');
    DOM.tabContentEditor.classList.remove('active');
  }
}

function openApiModal() {
  initApiModalValues();
  DOM.apiModal.classList.add('show');
}
function closeApiModal() {
  DOM.apiModal.classList.remove('show');
}

function saveApiConfig() {
  state.apiConfig.apiKey = DOM.apiKeyInput.value.trim();
  state.apiConfig.baseUrl = DOM.baseUrlInput.value.trim();
  state.apiConfig.modelName = DOM.modelNameInput.value.trim();
  state.apiConfig.protocol = DOM.apiProtocolSelect.value;
  state.apiConfig.concurrency = parseInt(DOM.concurrencySelect.value, 10);

  localStorage.setItem('scriptgenius_api_key', state.apiConfig.apiKey);
  localStorage.setItem('scriptgenius_base_url', state.apiConfig.baseUrl);
  localStorage.setItem('scriptgenius_model_name', state.apiConfig.modelName);

  updateApiStatusIndicator();
  updateModelInfoFooter();
  closeApiModal();
  showToast('API 参数设置已更新并成功保存', 'success');
}

async function fetchModelsList() {
  const baseUrl = DOM.baseUrlInput.value.trim();
  const apiKey = DOM.apiKeyInput.value.trim();

  if (!baseUrl || !apiKey) {
    showToast('请先填写 Base URL 和 API Key 才能拉取模型列表！', 'error');
    return;
  }

  showToast('正在向新站点拉取可用模型列表...', 'info');
  DOM.btnFetchModels.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 拉取中...`;

  try {
    const cleanUrl = baseUrl.replace(/\/+$/, '');
    const url = `${cleanUrl}/models`;
    const res = await fetch(url, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    let modelIds = [];

    if (Array.isArray(data.data)) {
      modelIds = data.data.map(item => item.id || item.name).filter(Boolean);
    } else if (Array.isArray(data.models)) {
      modelIds = data.models.map(item => (item.name || item.id).replace(/^models\//, '')).filter(Boolean);
    }

    if (modelIds.length > 0) {
      populateModelsDropdown(modelIds);
      showToast(`🎉 成功拉取 ${modelIds.length} 个模型！已同步填充至选择列表`, 'success');
    } else {
      showToast('未拉取到模型列表，可手动输入', 'warning');
    }
  } catch (err) {
    showToast(`拉取模型列表失败: ${err.message}`, 'error');
  } finally {
    DOM.btnFetchModels.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> 拉取可用模型列表`;
  }
}

function populateModelsDropdown(modelIds) {
  DOM.fetchedModelsWrapper.style.display = 'block';
  DOM.fetchedModelsSelect.innerHTML = `<option value="">-- 从拉取的 ${modelIds.length} 个模型中直接选择 --</option>`;
  DOM.modelsDatalist.innerHTML = '';

  modelIds.forEach(id => {
    const optData = document.createElement('option');
    optData.value = id;
    DOM.modelsDatalist.appendChild(optData);

    const optSelect = document.createElement('option');
    optSelect.value = id;
    optSelect.textContent = id;
    DOM.fetchedModelsSelect.appendChild(optSelect);
  });
}

async function testApiConnection() {
  const key = DOM.apiKeyInput.value.trim();
  const baseUrl = DOM.baseUrlInput.value.trim();
  const model = DOM.modelNameInput.value.trim() || 'qwen-vl-max';

  if (!key || !baseUrl) {
    showToast('请先填写 API Key 和 Base URL', 'error');
    return;
  }

  showToast(`正在测试模型 [${model}] 的接口与参数...`, 'info');

  try {
    const cleanUrl = baseUrl.replace(/\/+$/, '');
    const url = `${cleanUrl}/chat/completions`;
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model: model,
        messages: [{ role: 'user', content: 'hi' }],
        max_tokens: 5
      })
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok && !data.error) {
      showToast(`✅ 模型 [${model}] 连接与参数校验成功！可用通畅`, 'success');
    } else {
      const errMsg = data.error?.message || `HTTP ${res.status}`;
      showToast(`⚠️ 模型 [${model}] 校验失败: ${errMsg}`, 'error');
    }
  } catch (err) {
    showToast(`❌ API 连接失败: ${err.message}`, 'error');
  }
}

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>${escapeHtml(message)}</span>`;
  DOM.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.floor(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}



// ====== 用户鉴权与历史数据隔离 ======
var currentAuthTab = 'login';

function getToken() {
  return localStorage.getItem('auth_token') || '';
}

function getAuthHeaders() {
  var t = getToken();
  return t ? { 'Authorization': 'Bearer ' + t } : {};
}

function openAuthModal() {
  document.getElementById('authModal').style.display = 'flex';
  document.getElementById('authErrMsg').style.display = 'none';
}

function closeAuthModal() {
  document.getElementById('authModal').style.display = 'none';
}

function switchAuthTab(tab) {
  currentAuthTab = tab;
  document.getElementById('authErrMsg').style.display = 'none';
  if (tab === 'login') {
    document.getElementById('authTabLogin').classList.add('active');
    document.getElementById('authTabRegister').classList.remove('active');
    document.getElementById('authSubmitBtn').innerText = '🔑 立即登录';
  } else {
    document.getElementById('authTabRegister').classList.add('active');
    document.getElementById('authTabLogin').classList.remove('active');
    document.getElementById('authSubmitBtn').innerText = '✨ 注册新账号';
  }
}

async function checkAuthStatus() {
  var token = getToken();
  if (!token) {
    openAuthModal();
    updateUserBadge(null);
    return;
  }
  try {
    var r = await fetch('/api/auth/me?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
    var d = await r.json();
    if (d.user && d.user.username) {
      updateUserBadge(d.user.username);
      closeAuthModal();
      loadBabenHistory();
    } else {
      openAuthModal();
      updateUserBadge(null);
    }
  } catch (e) {
    updateUserBadge(null);
  }
}

function updateUserBadge(username) {
  if (username) {
    document.getElementById('userNameShow').innerHTML = '👤 ' + username;
    document.getElementById('userAuthActionBtn').innerText = '🚪 退出';
    document.getElementById('userAuthActionBtn').onclick = logoutUser;
  } else {
    document.getElementById('userNameShow').innerHTML = '👤 未登录';
    document.getElementById('userAuthActionBtn').innerText = '🔑 登录';
    document.getElementById('userAuthActionBtn').onclick = openAuthModal;
  }
}

async function submitAuth() {
  var u = document.getElementById('authUsername').value.trim();
  var p = document.getElementById('authPassword').value.trim();
  var errBox = document.getElementById('authErrMsg');
  errBox.style.display = 'none';

  if (!u || !p) {
    errBox.innerText = '用户名和密码不能为空！';
    errBox.style.display = 'block';
    return;
  }

  var endpoint = currentAuthTab === 'login' ? '/api/auth/login' : '/api/auth/register';
  try {
    var r = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p })
    });
    var d = await r.json();
    if (d.status === 'ok') {
      localStorage.setItem('auth_token', d.token);
      localStorage.setItem('auth_username', d.username);
      showToast(currentAuthTab === 'login' ? '🎉 登录成功！' : '🎉 注册成功并已登录！', 'success');
      closeAuthModal();
      checkAuthStatus();
    } else {
      errBox.innerText = d.message || '操作失败，请重试';
      errBox.style.display = 'block';
    }
  } catch (e) {
    errBox.innerText = '连接服务器失败：' + e.message;
    errBox.style.display = 'block';
  }
}

function logoutUser() {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_username');
    updateUserBadge(null);
    openAuthModal();
  }
}

async function loadBabenHistory() {
  var token = getToken();
  if (!token) return;
  try {
    var r = await fetch('/api/baben/history/list?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
    var d = await r.json();
    var container = document.getElementById('babenHistoryList');
    if (container) {
      if (d.records && d.records.length) {
        container.innerHTML = d.records.map(function(item) {
          return '<div style="padding:6px 8px;margin-bottom:4px;border-radius:6px;background:var(--input-bg);border:1px solid var(--input-border);cursor:pointer;display:flex;justify-content:space-between;align-items:center;" onclick="viewBabenHistoryDetail(' + item.id + ')">' +
            '<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px;" title="' + item.video_name + '">📜 ' + item.video_name + '</span>' +
            '<span style="font-size:10px;opacity:0.6;">查看</span></div>';
        }).join('');
      } else {
        container.innerHTML = '<div style="padding:8px;opacity:0.6;">暂无扒本历史</div>';
      }
    }
  } catch(e) {}
}

async function viewBabenHistoryDetail(historyId) {
  var token = getToken();
  try {
    var r = await fetch('/api/baben/history/detail/' + historyId + '?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
    var d = await r.json();
    if (d.status === 'ok' && d.script_text) {
      DOM.scriptTextarea.value = d.script_text;
      handleEditorInput();
      showToast('📖 已成功载入历史剧本：' + d.video_name, 'success');
    }
  } catch (e) {
    showToast('载入历史剧本失败：' + e.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  checkAuthStatus();
});
