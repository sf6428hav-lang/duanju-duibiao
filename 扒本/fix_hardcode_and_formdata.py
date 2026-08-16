import os, re

d = r'C:\Users\Administrator\Desktop\扒本'

# 1. Update index.html
index_p = os.path.join(d, 'index.html')
with open(index_p, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace BACKEND_URL
html = html.replace('const BACKEND_URL = "http://127.0.0.1:8080";', 'const BACKEND_URL = window.location.origin;')
html = html.replace('const BACKEND_URL = "http://localhost:8080";', 'const BACKEND_URL = window.location.origin;')

# Clean up status banners
html = html.replace('🔍 检查本地 Python 后端服务中 (http://localhost:8080)...', '🔍 正在连接后端 Python 服务...')
html = html.replace('🟢 本地 Python 代理后端已正常运行 (http://localhost:8080)', '🟢 后端 Python 服务运行正常 (' + ')' )
html = html.replace('🟡 未检测到本地 Python 后端 (端口 8080)', '🟡 无法连接到后端服务')
html = html.replace('http://localhost:8080', '当前服务地址')

with open(index_p, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.js
app_p = os.path.join(d, 'app.js')
with open(app_p, 'r', encoding='utf-8') as f:
    js = f.read()

# Clean analyzeVideoFile to 100% FormData upload ONLY
old_analyze = """async function analyzeVideoFile(fileObj) {
  const promptText = state.customPrompts[state.currentPresetKey];
  const liveBaseUrl = (DOM.baseUrlInput.value.trim() || state.apiConfig.baseUrl).replace(/\\/+$/, '');
  const liveApiKey = DOM.apiKeyInput.value.trim() || state.apiConfig.apiKey;
  const model = DOM.modelNameInput.value.trim() || state.apiConfig.modelName || 'qwen-vl-max';

  if (!liveBaseUrl || !liveApiKey) {
    throw new Error('未设置 API 地址或 Key，请在右上角【API 接口设置】中配置新站点');
  }

  if (state.activeFileId === fileObj.id) {
    DOM.scriptTextarea.value = '';
    handleEditorInput();
  }

  showToast(`正在开启 Python 1:1 全量剧本提取... [${fileObj.name}]`, 'info');

  let response;
  if (fileObj.file && fileObj.file instanceof File) {
    const formData = new FormData();
    formData.append('video', fileObj.file);
    formData.append('token', getToken());
    formData.append('api_key', liveApiKey);
    formData.append('base_url', liveBaseUrl);
    formData.append('model', model);
    formData.append('prompt', promptText);
    formData.append('no_slice', 'true');
    formData.append('episode_num', '1');

    response = await fetch('/api/upload_and_analyze', {
      method: 'POST',
      body: formData
    });
  } else {
    response = await fetch('/api/analyze_native_stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file_path: fileObj.file.path || fileObj.name,
        api_key: liveApiKey,
        base_url: liveBaseUrl,
        model: model,
        prompt: promptText
      })
    });
  }"""

new_analyze = """async function analyzeVideoFile(fileObj) {
  const promptText = state.customPrompts[state.currentPresetKey];
  const liveBaseUrl = (DOM.baseUrlInput.value.trim() || state.apiConfig.baseUrl).replace(/\\/+$/, '');
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
  });"""

if old_analyze in js:
    js = js.replace(old_analyze, new_analyze)
else:
    # Use regex to find analyzeVideoFile block and replace it cleanly
    pattern = r'async function analyzeVideoFile\(fileObj\) \{[\s\S]*?response = await fetch\([^\)]+\);\s*\}'
    js = re.sub(pattern, new_analyze, js)

with open(app_p, 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Synchronize server.py to match main.py in 扒本
main_p = os.path.join(d, 'main.py')
server_p = os.path.join(d, 'server.py')
with open(main_p, 'r', encoding='utf-8') as f:
    main_code = f.read()

with open(server_p, 'w', encoding='utf-8') as f:
    f.write(main_code)

print("Fixes applied successfully to index.html, app.js, and server.py!")
