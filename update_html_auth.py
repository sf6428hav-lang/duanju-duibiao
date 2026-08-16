import os

d = r'C:\Users\Administrator\Desktop\短剧对标'
index_p = os.path.join(d, 'index.html')

with open(index_p, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Auth CSS to <style>
auth_css = """
    /* 用户登录注册弹窗 */
    .auth-overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(8px);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      animation: fadeIn 0.3s ease;
    }
    .auth-card {
      background: var(--card, #ffffff);
      border: 1px solid var(--border, #e2e8f0);
      border-radius: 20px;
      width: 400px;
      max-width: 90vw;
      padding: 24px 28px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    .auth-tabs {
      display: flex;
      margin-bottom: 20px;
      border-bottom: 2px solid var(--border, #e2e8f0);
    }
    .auth-tab-btn {
      flex: 1;
      padding: 10px;
      text-align: center;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-muted, #64748b);
      border-bottom: 2px solid transparent;
      margin-bottom: -2px;
      transition: all 0.2s;
    }
    .auth-tab-btn.active {
      color: var(--primary, #2563eb);
      border-bottom-color: var(--primary, #2563eb);
    }
    .auth-input-group {
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .auth-input-group label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted, #64748b);
    }
"""

if '.auth-overlay' not in html:
    html = html.replace('</style>', auth_css + '\n  </style>')

# Add Auth Modal HTML right after <body>
auth_html = """
  <!-- 用户登录注册弹窗 -->
  <div id="authModal" class="auth-overlay" style="display:none;">
    <div class="auth-card">
      <div style="text-align:center;margin-bottom:16px;">
        <h3 style="font-size:20px;margin-bottom:4px;">🎬 创作工坊用户系统</h3>
        <p style="font-size:12px;opacity:0.7;">登入专属账号，自动隔离与多端同步您的短剧资产</p>
      </div>

      <div class="auth-tabs">
        <div id="authTabLogin" class="auth-tab-btn active" onclick="switchAuthTab('login')">🔑 账号登录</div>
        <div id="authTabRegister" class="auth-tab-btn" onclick="switchAuthTab('register')">✨ 注册新账号</div>
      </div>

      <div id="authErrMsg" style="display:none;color:#ef4444;background:#fee2e2;padding:8px 12px;border-radius:8px;font-size:12px;margin-bottom:12px;"></div>

      <div class="auth-input-group">
        <label>用户名 / 账号</label>
        <input type="text" id="authUsername" class="input-box" placeholder="请输入用户名 (如: admin)" autocomplete="off">
      </div>

      <div class="auth-input-group">
        <label>密码</label>
        <input type="password" id="authPassword" class="input-box" placeholder="请输入密码" autocomplete="off" onkeydown="if(event.key==='Enter') submitAuth()">
      </div>

      <button id="authSubmitBtn" class="btn primary full" style="margin-top:16px;padding:10px;font-size:14px;" onclick="submitAuth()">立即登录</button>
      <div style="text-align:center;margin-top:12px;font-size:12px;opacity:0.6;">默认初始账号: admin / nPB5hKpCu3NnruO1</div>
    </div>
  </div>
"""

if 'id="authModal"' not in html:
    html = html.replace('<body>', '<body>\n' + auth_html)

# Add User Badge to Sidebar
user_badge = """
    <div id="userBadge" style="margin-bottom:12px;padding:8px 12px;background:var(--bg2);border:1px solid var(--border);border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
      <span id="userNameShow" style="font-size:13px;font-weight:600;">👤 未登录</span>
      <button id="userAuthActionBtn" class="btn xs" onclick="openAuthModal()">登录/注册</button>
    </div>
"""

if 'id="userBadge"' not in html:
    html = html.replace('<h3>🎬 创作工坊</h3>', '<h3>🎬 创作工坊</h3>\n' + user_badge)

# Add Auth JS Logic before </body>
auth_js = """
    // ====== 用户鉴权与历史同步逻辑 ======
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
        var r = await fetch(B + '/api/auth/me?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
        var d = await r.json();
        if (d.user && d.user.username) {
          updateUserBadge(d.user.username);
          closeAuthModal();
          loadUserHistorySessions();
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
        document.getElementById('userNameShow').innerHTML = '👤 ' + esc(username);
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
        var r = await fetch(B + endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: u, password: p })
        });
        var d = await r.json();
        if (d.status === 'ok') {
          localStorage.setItem('auth_token', d.token);
          localStorage.setItem('auth_username', d.username);
          showToast(currentAuthTab === 'login' ? '🎉 登录成功！' : '🎉 注册成功并已登录！');
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

    async function loadUserHistorySessions() {
      var token = getToken();
      if (!token) return;
      try {
        var r = await fetch(B + '/api/history/list?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
        var d = await r.json();
        if (d.sessions && d.sessions.length) {
          var sel = document.getElementById('historySelect');
          if (sel) {
            sel.innerHTML = d.sessions.map(function(s) {
              return '<option value="' + s.session_id + '">' + esc(s.title) + '</option>';
            }).join('');
          }
        }
      } catch(e) {}
    }
"""

if 'function checkAuthStatus()' not in html:
    html = html.replace('ld(); lds(); rf();', auth_js + '\n    ld(); lds(); rf(); checkAuthStatus();')

with open(index_p, 'w', encoding='utf-8') as f:
    f.write(html)

with open(os.path.join(d, '创作工坊.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print("Auth JS & CSS injected into index.html and 创作工坊.html successfully!")
