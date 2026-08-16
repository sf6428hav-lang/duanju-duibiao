import os

d = r'C:\Users\Administrator\Desktop\扒本'
index_p = os.path.join(d, 'index.html')
app_p = os.path.join(d, 'app.js')

with open(index_p, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Auth CSS
auth_css = """
    .auth-overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(8px);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .auth-card {
      background: var(--card-bg, #ffffff);
      border: var(--card-border, 1px solid #e2e8f0);
      border-radius: 20px;
      width: 400px;
      max-width: 90vw;
      padding: 24px 28px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    .auth-tabs {
      display: flex;
      margin-bottom: 20px;
      border-bottom: 2px solid var(--card-border, #e2e8f0);
    }
    .auth-tab-btn {
      flex: 1;
      padding: 10px;
      text-align: center;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-sub, #64748b);
      border-bottom: 2px solid transparent;
      margin-bottom: -2px;
    }
    .auth-tab-btn.active {
      color: var(--primary-color, #2563eb);
      border-bottom-color: var(--primary-color, #2563eb);
    }
    .auth-input-group {
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
"""

if '.auth-overlay' not in html:
    html = html.replace('</style>', auth_css + '\n  </style>')

# Add Auth Modal HTML
auth_html = """
  <!-- 用户登录注册弹窗 -->
  <div id="authModal" class="auth-overlay" style="display:none;">
    <div class="auth-card">
      <div style="text-align:center;margin-bottom:16px;">
        <h3 style="font-size:20px;margin-bottom:4px;">🎬 扒本工作台 · 用户系统</h3>
        <p style="font-size:12px;opacity:0.7;">登录统一账号，隔离保存您的扒本剧本历史</p>
      </div>

      <div class="auth-tabs">
        <div id="authTabLogin" class="auth-tab-btn active" onclick="switchAuthTab('login')">🔑 账号登录</div>
        <div id="authTabRegister" class="auth-tab-btn" onclick="switchAuthTab('register')">✨ 注册新账号</div>
      </div>

      <div id="authErrMsg" style="display:none;color:#ef4444;background:#fee2e2;padding:8px 12px;border-radius:8px;font-size:12px;margin-bottom:12px;"></div>

      <div class="auth-input-group">
        <label style="font-size:12px;">用户名 / 账号</label>
        <input type="text" id="authUsername" class="api-modal-input" placeholder="请输入用户名 (如: admin)" autocomplete="off">
      </div>

      <div class="auth-input-group">
        <label style="font-size:12px;">密码</label>
        <input type="password" id="authPassword" class="api-modal-input" placeholder="请输入密码" autocomplete="off" onkeydown="if(event.key==='Enter') submitAuth()">
      </div>

      <button id="authSubmitBtn" class="btn-primary-gradient" style="width:100%;margin-top:16px;padding:10px;font-size:14px;" onclick="submitAuth()">🔑 立即登录</button>
      <div style="text-align:center;margin-top:12px;font-size:12px;opacity:0.6;">默认初始账号: admin / nPB5hKpCu3NnruO1</div>
    </div>
  </div>
"""

if 'id="authModal"' not in html:
    html = html.replace('<body>', '<body>\n' + auth_html)

# Add Top Bar User Badge
user_badge = """
    <div id="userBadge" style="margin-right:12px;padding:4px 10px;background:var(--card-bg);border:var(--card-border);border-radius:8px;display:flex;align-items:center;gap:8px;">
      <span id="userNameShow" style="font-size:12px;font-weight:600;">👤 未登录</span>
      <button id="userAuthActionBtn" class="btn-action-mini" onclick="openAuthModal()">登录/注册</button>
    </div>
"""

if 'id="userBadge"' not in html:
    html = html.replace('<div class="header-control-bar">', '<div class="header-control-bar">\n' + user_badge)

# Add History Block to Sidebar
history_block = """
      <!-- 📚 扒本历史与剧本库 -->
      <div class="sidebar-block">
        <div class="sidebar-header">
          <span>📚 我的扒本历史</span>
          <button class="btn-action-mini" onclick="loadBabenHistory()">🔄 刷新</button>
        </div>
        <div id="babenHistoryList" class="session-list" style="max-height:160px;overflow-y:auto;font-size:12px;">
          <div style="padding:8px;opacity:0.6;">暂无扒本历史</div>
        </div>
      </div>
"""

if 'id="babenHistoryList"' not in html:
    html = html.replace('<div class="sidebar-block" style="flex: 1; display: flex; flex-direction: column;">', history_block + '\n<div class="sidebar-block" style="flex: 1; display: flex; flex-direction: column;">')

with open(index_p, 'w', encoding='utf-8') as f:
    f.write(html)

# Now update app.js
with open(app_p, 'r', encoding='utf-8') as f:
    js_code = f.read()

# Add formData.append('token', getToken())
if "formData.append('token'," not in js_code:
    js_code = js_code.replace("formData.append('video', fileObj.file);", "formData.append('video', fileObj.file);\n    formData.append('token', getToken());")

auth_app_js = """
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
"""

if 'function checkAuthStatus()' not in js_code:
    js_code += '\n\n' + auth_app_js

with open(app_p, 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Baben Auth & User Data Isolation injected successfully!")
