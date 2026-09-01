
    var B = (window.location.origin === 'file://' || window.location.origin === 'null') ? 'http://localhost:8000' : window.location.origin;
    var TH = {
      "🍑 蜜桃乌龙": { bg: "#faf7f5", bg2: "#ffffff", text: "#332927", primary: "#e07a5f", card: "#ffffff", border: "#f0e6e1", shadow: "0 4px 16px rgba(224,122,95,0.08)", radius: "12px", eb: "#fdf2f2", ebd: "#f8b4b4", dot: "#e07a5f", stepDone: "#10b981", stepActive: "#e07a5f", stepPending: "#d1d5db" },
      "🌿 薄荷暗色": { bg: "#1e2328", bg2: "#161a1e", text: "#d0d6d8", primary: "#68b893", card: "#262c32", border: "#353d45", shadow: "0 4px 20px rgba(0,0,0,0.25)", radius: "10px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#68b893", stepDone: "#34d399", stepActive: "#68b893", stepPending: "#4b5563" },
      "🫐 蓝莓暗夜": { bg: "#1a1d2e", bg2: "#141726", text: "#c8cddb", primary: "#7c8ce0", card: "#232740", border: "#353b58", shadow: "0 4px 20px rgba(0,0,0,0.30)", radius: "10px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#7c8ce0", stepDone: "#34d399", stepActive: "#7c8ce0", stepPending: "#4b5563" },
      "🖤 曜石极简": { bg: "#111111", bg2: "#0a0a0a", text: "#cccccc", primary: "#eeeeee", card: "#1a1a1a", border: "#333333", shadow: "0 4px 20px rgba(0,0,0,0.40)", radius: "4px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#eeeeee", stepDone: "#22c55e", stepActive: "#eeeeee", stepPending: "#555555" },
      "🍷 醉红香槟": { bg: "#fdfbf7", bg2: "#ffffff", text: "#2d2424", primary: "#c05621", card: "#ffffff", border: "#f3ebd9", shadow: "0 4px 16px rgba(192,86,33,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#c05621", stepDone: "#38a169", stepActive: "#c05621", stepPending: "#cbd5e0" },
      "🌌 极光深空": { bg: "#0f172a", bg2: "#0b1120", text: "#e2e8f0", primary: "#38bdf8", card: "#1e293b", border: "#334155", shadow: "0 4px 20px rgba(0,0,0,0.35)", radius: "10px", eb: "#451a1a", ebd: "#f87171", dot: "#38bdf8", stepDone: "#34d399", stepActive: "#38bdf8", stepPending: "#64748b" },
      "🍵 静心抹茶": { bg: "#f4f7f4", bg2: "#ffffff", text: "#243224", primary: "#48bb78", card: "#ffffff", border: "#e2ebe2", shadow: "0 4px 16px rgba(72,187,120,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#48bb78", stepDone: "#38a169", stepActive: "#48bb78", stepPending: "#cbd5e0" },
      "🍊 焦糖琥珀": { bg: "#fefcf9", bg2: "#ffffff", text: "#3c2a1e", primary: "#dd6b20", card: "#ffffff", border: "#fbd5c0", shadow: "0 4px 16px rgba(221,107,32,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#dd6b20", stepDone: "#38a169", stepActive: "#dd6b20", stepPending: "#cbd5e0" },
      "🌃 霓虹夜幕": { bg: "#13111c", bg2: "#0d0b14", text: "#dcd7ec", primary: "#a855f7", card: "#1c182b", border: "#2e2844", shadow: "0 4px 20px rgba(0,0,0,0.35)", radius: "10px", eb: "#3b1219", ebd: "#f43f5e", dot: "#a855f7", stepDone: "#10b981", stepActive: "#a855f7", stepPending: "#6b7280" },
      "🩶 莫兰迪灰": { bg: "#f0f2f5", bg2: "#ffffff", text: "#2c3e50", primary: "#64748b", card: "#ffffff", border: "#cbd5e1", shadow: "0 4px 16px rgba(100,116,139,0.08)", radius: "8px", eb: "#fef2f2", ebd: "#fca5a5", dot: "#64748b", stepDone: "#10b981", stepActive: "#64748b", stepPending: "#94a3b8" }
    };

    
    let currentPreviewFile = "";
      E("editorContent").contentEditable = "false";
      E("editorContent").innerHTML = '<p style="color:#999; text-align:center; margin-top:100px; user-select:none; pointer-events:none;">👈 在左侧选择或上传文件，开始编辑...</p>';
      updateWordCount();

    function updateWordCount() {
      var text = E('editorContent').innerText || "";
      var count = text.replace(/\s/g, '').length;
      E('editorWordCountStr').innerText = '字数：' + count;
      E('editorSaveStatus').innerText = '未保存';
      E('editorSaveStatus').style.color = '#ef4444';
    }

    async function saveEditorContent() {
      if(!currentPreviewFile) return;
      var text = E('editorContent').innerText;
      E('editorSaveStatus').innerText = '保存中...';
      try {
        var r = await fetch(B + '/api/save_file', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': localStorage.getItem('sdt_token') || '' },
          body: JSON.stringify({ filepath: currentPreviewFile, content: text })
        });
        var d = await r.json();
        if (d.status === 'ok') {
          E('editorSaveStatus').innerText = '已保存';
          E('editorSaveStatus').style.color = '#10b981';
          showToast('保存成功');
        } else {
          alert('保存失败: ' + d.error);
        }
      } catch(e) {
        alert('保存失败: ' + e.message);
      }
    }

    function closeEditor() {
      
      currentPreviewFile = "";
      E("editorContent").contentEditable = "false";
      E("editorContent").innerHTML = '<p style="color:#999; text-align:center; margin-top:100px; user-select:none; pointer-events:none;">👈 在左侧选择或上传文件，开始编辑...</p>';
      updateWordCount();
    }

    // 对标流程 8 步定义
    var BENCH_STEPS = [
      { id: 1, icon: '📤', label: '上传参考' },
      { id: 2, icon: '🔍', label: '拆解分析' },
      { id: 3, icon: '📋', label: '提取模板' },
      { id: 4, icon: '🎯', label: '仿写方案' },
      { id: 5, icon: '📝', label: '生成大纲' },
      { id: 6, icon: '✅', label: '大纲确认' },
      { id: 7, icon: '📐', label: '格式确认' },
      { id: 8, icon: '🎬', label: '生成剧本' }
    ];

    // 每步的预设 prompt
    var STEP_PROMPTS = {
      1: '请帮我对标分析我上传的参考剧本，先确认已收到并阅读完毕。',
      2: '请对参考剧本进行逐集拆解分析（拉片），提取每集的情节节拍、钩子设计、情绪曲线、节奏量化指标。',
      3: '请基于拆解结果，提取可复用的结构模板，包括：剧情节拍公式、人物弧光模式、每集钩子位置与类型、付费留客悬念设计。',
      4: null,
      5: '请基于确认的仿写方案，生成仿写短剧的分集大纲。',
      6: null,
      7: null,
      8: '请按照确认的格式，开始逐集生成完整剧本。'
    };

    var S = { cid: 'c' + Date.now(), mode: null, chats: [], doc: '', s4: false, s7: false, cstr: false, qaHandled: false, cardsVisible: true, bi: 0, tb: 0, gen: false, ab: null, sd: null, edi: null, step4Questions: null, createStage: '头脑风暴', benchStep: 1 };

    function E(id) { return document.getElementById(id); }
    function esc(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

    function showToast(msg) {
      var t = document.createElement('div');
      t.className = 'toast-msg';
      t.innerText = msg;
      document.body.appendChild(t);
      setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 2000);
    }

    function sv() {
      var curC = CC();
      curC.step4Questions = S.step4Questions;
      curC.cstr = S.cstr;
      curC.qaHandled = S.qaHandled;
      curC.cardsVisible = (S.cardsVisible !== false);
      localStorage.setItem('app', JSON.stringify({ v: 'v55', cid: S.cid, mode: S.mode, chats: S.chats, s4: S.s4, s7: S.s7, cstr: S.cstr, qaHandled: S.qaHandled, cardsVisible: S.cardsVisible, bi: S.bi, tb: S.tb, sd: S.sd, createStage: S.createStage, benchStep: S.benchStep }));
    }

    function ld() {
      try {
        var raw = localStorage.getItem('app');
        if (raw) {
          var d = JSON.parse(raw);
          if (d) {
            S.cid = d.cid || S.cid; S.mode = d.mode; S.chats = d.chats || []; S.s4 = d.s4 || false; S.s7 = d.s7 || false; S.cstr = d.cstr || false; S.qaHandled = d.qaHandled || false; S.cardsVisible = (d.cardsVisible !== false); S.bi = d.bi || 0; S.tb = d.tb || 0; S.sd = d.sd; S.createStage = d.createStage || '头脑风暴'; S.benchStep = d.benchStep || 1;
            var curC = S.chats.find(function(x){ return x.id === S.cid; });
            S.step4Questions = curC ? (curC.step4Questions || null) : null;
          }
        }
      } catch (e) { }
    }

    function svs() {
      var mVal = E('customModel').value.trim() || E('modelSelect').value;
      localStorage.setItem('apis', JSON.stringify({ k: E('apiKey').value, u: E('apiUrl').value, m: mVal }));
      updateApiStatus();
    }

    function lds() {
      try {
        var d = JSON.parse(localStorage.getItem('apis'));
        if (d) {
          if (d.k !== undefined) E('apiKey').value = d.k;
          if (d.u !== undefined) E('apiUrl').value = d.u || 'https://yunwu.ai/v1';
          if (d.m) {
            var opts = E('modelSelect').options, has = false;
            for (var i = 0; i < opts.length; i++) {
              if (opts[i].value === d.m) { E('modelSelect').value = d.m; has = true; break; }
            }
            if (!has) E('customModel').value = d.m;
          }
        }
      } catch (e) { }
      updateApiStatus();
    }

    function updateApiStatus() {
      var k = E('apiKey').value.trim(), st = E('apiStatus');
      if (!k) { st.className = 'status-tag err'; st.innerHTML = '🔴 未设置Key'; }
      else { st.className = 'status-tag ok'; st.innerHTML = '🟢 已准备'; }
    }

    function gM() { return E('customModel').value.trim() || E('modelSelect').value || 'gpt-4o'; }
    function gK() { return E('apiKey').value.trim(); }
    function gU() { return E('apiUrl').value.trim() || 'https://yunwu.ai/v1'; }

    
    function toggleMultiSelect() {
      S.multiSelectMode = !S.multiSelectMode;
      S.selectedMsgs = {};
      rd();
    }
    
    function toggleSelectMsg(idx) {
      S.selectedMsgs[idx] = !S.selectedMsgs[idx];
      rd();
    }
    
    function deleteSelectedMsgs() {
      var c = CC();
      var toDelete = Object.keys(S.selectedMsgs).filter(function(k) { return S.selectedMsgs[k]; }).map(Number);
      if (toDelete.length === 0) {
        alert("请先选择要删除的消息");
        return;
      }
      if (!confirm("确定要删除选中的 " + toDelete.length + " 条消息吗？删除后AI将丢失这段记忆。")) return;
      
      toDelete.sort(function(a,b) { return b - a; });
      for (var i = 0; i < toDelete.length; i++) {
        c.msgs.splice(toDelete[i], 1);
      }
      S.multiSelectMode = false;
      S.selectedMsgs = {};
      sv(); rd();
    }

    function CC() {
      if (!S.chats) S.chats = [];
      var c = S.chats.find(function (x) { return x.id === S.cid; });
      if (!c) {
        c = { id: S.cid, title: '新对话', msgs: [], sd: null, mode: S.mode, benchStep: 1, step4Questions: null, cstr: false, qaHandled: false, cardsVisible: true };
        S.chats.unshift(c);
      }
      return c;
    }

    function cleanEmptyChats() {
      if (!S.chats) return;
      S.chats = S.chats.filter(function (c) {
        return (c.id === S.cid) || (c.msgs && c.msgs.length > 0);
      });
    }

    function newChat() {
      var curC = CC();
      if (curC.msgs && curC.msgs.length) {
        var f = curC.msgs.find(function (m) { return m.role === 'user'; });
        curC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
      }
      curC.mode = S.mode; curC.sd = S.sd; curC.benchStep = S.benchStep; curC.s4 = S.s4; curC.s7 = S.s7; curC.step4Questions = S.step4Questions; curC.cstr = S.cstr; curC.qaHandled = S.qaHandled; curC.cardsVisible = S.cardsVisible;

      cleanEmptyChats();

      var newId = 'c' + Date.now();
      var keepMode = S.mode;

      var newC = {
        id: newId,
        title: '新对话',
        msgs: [],
        sd: null,
        mode: keepMode,
        benchStep: 1,
        s4: false,
        s7: false,
        cstr: false,
        qaHandled: false,
        cardsVisible: true,
        step4Questions: null
      };

      S.chats.unshift(newC);
      S.cid = newId;
      S.mode = keepMode; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.tb = 0; S.sd = null; S.step4Questions = null; S.benchStep = 1; S.gen = false;

      sv();

      var inp = E('chatInput'); if (inp) inp.value = '';
      var area = E('chatArea'); if (area) area.innerHTML = '';
      
      ['createPanel', 'step4Panel', 'step7Panel', 'batchPanel'].forEach(function(id) {
        var p = E(id);
        if (p) { p.style.display = 'none'; p.innerHTML = ''; }
      });

      rf();
      showToast('✨ 已成功为您创建全新对话！');
    }

    async function swChat(id) {
      if (id === S.cid) return;
      var curC = CC();
      if (curC.msgs && curC.msgs.length) {
        var f = curC.msgs.find(function (m) { return m.role === 'user'; });
        curC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
      }
      curC.mode = S.mode; curC.sd = S.sd; curC.benchStep = S.benchStep; curC.s4 = S.s4; curC.s7 = S.s7; curC.step4Questions = S.step4Questions; curC.cstr = S.cstr; curC.qaHandled = S.qaHandled; curC.cardsVisible = S.cardsVisible;
      
      cleanEmptyChats();
      sv();

      S.cid = id;
      var targetC = CC();

      var token = getToken();
      if (token) {
        try {
          var r = await fetch(B + '/api/history/detail/' + id + '?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
          var d = await r.json();
          if (d.status === 'ok' && d.messages) {
            if (d.messages.length > 0 || !targetC.msgs || targetC.msgs.length === 0) {
                targetC.msgs = d.messages;
              }
            if (d.messages.length > 0) {
              var f = d.messages.find(function (m) { return m.role === 'user'; });
              targetC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
            }
          }
        } catch(e) {}
      }
      S.mode = targetC.mode || null;
      S.sd = targetC.sd || null;
      S.s4 = targetC.s4 || false;
      S.s7 = targetC.s7 || false;
      S.cstr = targetC.cstr || false;
      S.qaHandled = targetC.qaHandled || false;
      S.cardsVisible = (targetC.cardsVisible !== false);
      S.bi = 0;
      S.step4Questions = targetC.step4Questions || null;
      S.benchStep = targetC.benchStep || 1;
      S.gen = false;

      sv(); rf();
    }

    function delChat(id) {
      S.chats = S.chats.filter(function (c) { return c.id !== id; });
      if (S.cid === id) {
        cleanEmptyChats();
        if (S.chats.length) swChat(S.chats[0].id);
        else newChat();
      } else { sv(); rf(); }
    }

    function openHistory() { renderHistory(); E('historyModal').classList.add('open'); }
    
    function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
    function closeSettings() { document.getElementById('settingsModal').style.display = 'none'; }

    function closeHistory() { E('historyModal').classList.remove('open'); }
    
    function renderHistorySelect() {
      var sel = E('historySelect');
      if (!sel) return;
      var list = S.chats || [];
      var h = '';
      for (var i = 0; i < list.length; i++) {
        var c = list[i], t = c.title || '对话 ' + (i + 1), is = (c.id === S.cid);
        h += '<option value="' + c.id + '" ' + (is ? 'selected' : '') + '>' + (is ? '👉 ' : '💬 ') + esc(t) + '</option>';
      }
      sel.innerHTML = h;
      sel.value = S.cid;
    }

    function renderHistory() {
      renderHistorySelect();
      var hl = E('historyModalList');
      if (!hl) return;
      var hc = '', list = S.chats || [];
      for (var i = 0; i < list.length; i++) {
        var c = list[i], t = c.title || '对话 ' + (i + 1), is = (c.id === S.cid), cnt = (c.msgs ? c.msgs.length : 0);
        hc += '<div class="modal-item ' + (is ? 'active' : '') + '" onclick="swChat(\'' + c.id + '\');closeHistory();"><div style="flex:1"><div style="font-weight:600;font-size:13px;' + (is ? 'color:var(--primary)' : '') + '">' + (is ? '👉 ' : '💬 ') + esc(t) + '</div><div style="font-size:11px;opacity:.5;margin-top:2px;">' + cnt + ' 条对话</div></div><button class="btn xs" onclick="event.stopPropagation();delChat(\'' + c.id + '\');renderHistory();" style="opacity:.5;">✕</button></div>';
      }
      hl.innerHTML = hc || '<div style="text-align:center;padding:30px 0;opacity:.4;font-size:13px;">暂无历史对话记录</div>';
    }

    function switchTheme(n) {
      var t = TH[n], r = document.documentElement.style;
      r.setProperty('--bg', t.bg); r.setProperty('--bg2', t.bg2); r.setProperty('--text', t.text);
      r.setProperty('--primary', t.primary); r.setProperty('--card', t.card); r.setProperty('--border', t.border);
      r.setProperty('--shadow', t.shadow); r.setProperty('--radius', t.radius); r.setProperty('--err-bg', t.eb);
      r.setProperty('--err-border', t.ebd); r.setProperty('--dot', t.dot);
      r.setProperty('--step-done', t.stepDone); r.setProperty('--step-active', t.stepActive); r.setProperty('--step-pending', t.stepPending);
      localStorage.setItem('theme', n);
    }

    // ====== 对标流程步骤条 ======
    function renderBenchSteps() {
      var bar = E('benchStepsBar'), inner = E('benchStepsInner');
      if (S.mode !== '短剧对标') { bar.classList.remove('show'); return; }
      bar.classList.add('show');
      var h = '';
      for (var i = 0; i < BENCH_STEPS.length; i++) {
        var s = BENCH_STEPS[i], cls = 'pending';
        if (s.id < S.benchStep) cls = 'done';
        else if (s.id === S.benchStep) cls = 'active';

        h += '<div class="step-item ' + cls + '" onclick="goBenchStep(' + s.id + ')" title="点击查看此步骤说明">';
        h += '<span class="step-num">' + (cls === 'done' ? '✓' : s.id) + '</span>';
        h += '<span>' + s.icon + ' ' + s.label + '</span>';
        h += '<span class="step-tip">' + getStepTip(s.id) + '</span>';
        h += '</div>';

        if (i < BENCH_STEPS.length - 1) {
          h += '<div class="step-connector' + (s.id < S.benchStep ? ' done' : '') + '"></div>';
        }
      }
      inner.innerHTML = h;
    }

    function getStepTip(id) {
      var tips = {
        1: '上传参考剧本（.docx或粘贴文本）',
        2: 'AI逐集拆解情节节拍与钩子',
        3: '提取可复用的结构模板',
        4: '确认仿写方案与改编方案',
        5: '基于模板生成仿写大纲',
        6: '审核并确认分集大纲',
        7: '设定剧本输出格式',
        8: '开始逐集生成完整剧本'
      };
      return tips[id] || '';
    }

    function goBenchStep(n) {
      if (n < S.benchStep) {
        var p = STEP_PROMPTS[n];
        if (p) { E('chatInput').value = p; E('chatInput').focus(); }
        return;
      }
      if (n === S.benchStep) {
        triggerCurrentStep();
        return;
      }
      alert('请先完成步骤 ' + S.benchStep + '（' + BENCH_STEPS[S.benchStep - 1].label + '）');
    }

    function triggerCurrentStep() {
      var step = S.benchStep;
      if (step === 1) {
        E('fileInput').click();
      } else if (step === 4 && tryParseS4()) {
        rP();
      } else if (step === 7 && S.s4) {
        rP();
      } else if (step === 8 && S.s7) {
        nB();
      } else {
        var p = STEP_PROMPTS[step];
        if (p) { E('chatInput').value = p; E('chatInput').focus(); }
      }
    }

    function advanceBenchStep(n) {
      if (n > S.benchStep) {
        S.benchStep = n;
        var c = CC(); c.benchStep = n;
        sv(); renderBenchSteps(); rP();
      }
    }

    // ====== 面板提取与动态捕获逻辑 =====
    function extractTJ(txt) {
      if (!txt) return null;
      var m = txt.match(/\[TEMPLATEJSON\]\s*([\s\S]*?)\s*\[\/TEMPLATEJSON\]/);
      if (m) { try { return JSON.parse(m[1].trim()); } catch (e) { } }
      var m2 = txt.match(/```json\s*([\s\S]*?)\s*```/);
      if (m2) { try { return JSON.parse(m2[1].trim()); } catch (e) { } }
      var m3 = txt.match(/\{[\s\S]*?"(?:step4_questions|create_questions|questions)"[\s\S]*?\}/);
      if (m3) { try { return JSON.parse(m3[0].trim()); } catch (e) { } }
      return null;
    }

    function stripThinking(txt) {
      if (!txt) return '';
      return txt.replace(/<thinking>[\s\S]*?<\/thinking>/gi, '').trim();
    }

    function detectOptions(txt) {
      if (!txt) return null;
      var cleanTxt = stripThinking(txt);
      if (!cleanTxt) return null;
      var blocks = [];
      var lines = cleanTxt.split('\n');
      var curQ = null;
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        if (!line) continue;

        if (/^(?:已保存|output_|```|===|---|📁|✨|🤖)/i.test(line)) {
          continue;
        }

        var optMatch = line.match(/^(?:[A-D][\.\)\s]|(?:\d+\))\s*|选项\s*[A-Z1-9][:：\s]?)\s*(.+)/i);
        if (optMatch && curQ) {
          var optText = optMatch[1].replace(/\*\*/g, '').trim();
          if (optText && optText.length >= 2 && optText.length < 200) {
            curQ.options.push(optText);
            continue;
          }
        }

        var isNumHeader = /^(?:\d+[\.、\s]|\*\*\d+[\.、\s]?|【?(?:问题|方向|确认点)\d+】?|Q\d+[:：\s]?)/i.test(line);
        var isQuestionEnd = line.endsWith('？') || line.endsWith('?') || line.endsWith('？）') || line.endsWith('?)');
        var hasQuestionVerb = /你觉得|是否|偏早还是偏晚|如何|哪种|要不要|请确认|倾向|单选|多选|请选择|审核/i.test(line);
        var isForbiddenTitle = /^(?:公式|模板|拆解表格|商业模型|代码块|json|templatejson|已确认|已保存|幻想画面|总结|纲要)/i.test(line);

        var isRealQuestion = (isQuestionEnd || hasQuestionVerb) && (isNumHeader || line.length <= 150);

        if (isRealQuestion && line.length >= 5 && line.length <= 200 && !isForbiddenTitle) {
          if (curQ) {
            if (!curQ.options || !curQ.options.length) {
              curQ.options = ["A. 认可并按此方案执行", "B. 需要微调（在下方框内说明）", "其他 (请在下方输入框补充说明)"];
            }
            blocks.push(curQ);
          }
          curQ = { question: line.replace(/\*\*/g, '').trim(), options: [] };
        }
      }
      if (curQ) {
        if (!curQ.options || !curQ.options.length) {
          curQ.options = ["A. 认可并按此方案执行", "B. 需要微调（在下方框内说明）", "其他 (请在下方输入框补充说明)"];
        }
        blocks.push(curQ);
      }
      return blocks.length ? blocks : null;
    }

    function tryParseS4() {
      var curC = CC();
      var msgs = curC.msgs;
      if (!msgs || !msgs.length) return null;

      // 每次只解析最后一条 AI 助手的消息！
      var lastM = null;
      for (var i = msgs.length - 1; i >= 0; i--) {
        if (msgs[i].role === 'assistant' && !msgs[i].er) {
          lastM = msgs[i];
          break;
        }
      }

      if (!lastM || !lastM.content) return null;
      // 如果该条消息已点击处理过，避免显示旧卡片
      if (lastM.handled) return null;

      // 🔴 剥离 AI 内部思考标签 <thinking>...</thinking>，防止将思考过程解析为面板卡片
      var txt = stripThinking(lastM.content);
      if (!txt) return null;

      var d = extractTJ(txt);
      if (d && (d.step4_questions || d.questions || d.step === 'step4_ready' || d.step === 'create_qa_ready')) {
        var qs = d.step4_questions || d.questions;
        if (qs && qs.length) {
          return { step: 'create_qa_ready', questions: qs, step4_questions: qs, msgId: lastM.id };
        }
      }

      return null;
    }

    function selectOpt(el, qi, optVal) {
      var parent = el.closest('.q-block');
      if (parent) {
        var opts = parent.querySelectorAll('.q-opt');
        for (var i = 0; i < opts.length; i++) opts[i].classList.remove('selected');
      }
      el.classList.add('selected');
      var rad = el.querySelector('input[type=radio]');
      if (rad) rad.checked = true;

      var customBox = E('q_custom_' + qi);
      if (customBox) {
        var isOther = /其他|自定义|其它|other|修改|混搭|说明|微调|补充/i.test(optVal);
        customBox.style.display = isOther ? 'block' : 'none';
        if (!isOther) customBox.value = '';
      }
    }

    function dismissCards() {
      S.cardsVisible = false;
      var curC = CC(); curC.cardsVisible = false;
      sv();
      E('createPanel').style.display = 'none';
    }

    function rP() {
      var cp = E('createPanel'), s4 = E('step4Panel'), s7 = E('step7Panel'), bp = E('batchPanel');

      // 🔴 剧本创作模式交互面板：只要 AI 输出 TEMPLATEJSON 或导引问题，动态展示选择面板
      if (S.mode === '剧本创作') {
        var chat = CC();
        var msgs = chat.msgs || [];
        var lastM = msgs.length ? msgs[msgs.length - 1] : null;

        if (S.gen || (lastM && lastM.role === 'user')) {
          cp.style.display = 'none';
          return;
        }

        var data = tryParseS4();
        if (data && (data.step === 'create_qa_ready' || data.step4_questions || data.questions)) {
          var qs = data.step4_questions || data.questions;
          if (qs && qs.length) {
            cp.style.display = 'block';
            var h = '<div class="panel scroll-panel" style="max-height:300px;overflow-y:auto;"><div style="font-weight:600;font-size:14px;color:var(--primary);margin-bottom:8px;position:sticky;top:0;background:var(--card);padding:4px 0;z-index:5;">🎨 💬 剧本创作 · 需求与方向确认 (请勾选创作倾向)</div>';
            for (var qi = 0; qi < qs.length; qi++) {
              var q = qs[qi];
              h += '<div class="q-block" style="margin-bottom:12px;"><div style="font-weight:600;font-size:13px;margin:6px 0;color:var(--text);">' + esc(q.question) + '</div>';
              if (q.options && q.options.length) {
                for (var oi = 0; oi < q.options.length; oi++) {
                  var opt = q.options[oi], sel = (oi === 0);
                  h += '<div class="q-opt ' + (sel ? 'selected' : '') + '" onclick="selectOpt(this, ' + qi + ', \'' + esc(opt).replace(/'/g, "\\'") + '\')"><input type="radio" name="cq_' + qi + '" value="' + esc(opt) + '" ' + (sel ? 'checked' : '') + '> <span>' + esc(opt) + '</span></div>';
                }
              }
              h += '<input type="text" class="input-box q-custom" id="q_custom_' + qi + '" placeholder="请输入你的自定义要求..." style="display:none;margin-top:6px;"></div>';
            }
            h += '<button class="btn primary full" onclick="confirmCreateQA()" style="margin-top:10px;position:sticky;bottom:0;z-index:5;">确认选项，提交AI处理</button></div>';
            cp.innerHTML = h;
            return;
          }
        }

        cp.style.display = 'none';
        cp.innerHTML = '';
        return;
      } else {
        cp.style.display = 'none';
      }

      // 2. 短剧对标 Step 4 面板 (完全不受影响)
      if (S.mode === '短剧对标' && !S.s4) {
        var data = tryParseS4();
        if (data && (data.step === 'step4_ready' || data.step4_questions || data.questions)) {
          s4.style.display = 'block';
          var h = '<div class="panel scroll-panel" style="max-height:300px;overflow-y:auto;"><div style="font-weight:600;font-size:14px;color:var(--primary);margin-bottom:8px;position:sticky;top:0;background:var(--card);padding:4px 0;z-index:5;">⚡ 💬 基于本剧深度思考提取的核心确认选项 (点击选项高亮)</div>';
          var qs = data.step4_questions || data.questions;
          if (qs && qs.length) {
            for (var qi = 0; qi < qs.length; qi++) {
              var q = qs[qi];
              h += '<div class="q-block" style="margin-bottom:12px;"><div style="font-weight:600;font-size:13px;margin:6px 0;color:var(--text);">' + esc(q.question) + '</div>';
              if (q.options && q.options.length) {
                for (var oi = 0; oi < q.options.length; oi++) {
                  var opt = q.options[oi], sel = (oi === 0);
                  h += '<div class="q-opt ' + (sel ? 'selected' : '') + '" onclick="selectOpt(this, ' + qi + ', \'' + esc(opt).replace(/'/g, "\\'") + '\')"><input type="radio" name="q_' + qi + '" value="' + esc(opt) + '" ' + (sel ? 'checked' : '') + '> <span>' + esc(opt) + '</span></div>';
                }
              }
              h += '<input type="text" class="input-box q-custom" id="q_custom_' + qi + '" placeholder="请输入你的自定义仿写要求..." style="display:none;margin-top:6px;"></div>';
            }
          } else {
            h += '<p style="font-size:12px;opacity:.7;margin-bottom:6px;">AI已提出问题，请在下方描述你的仿写方案：</p>';
          }
          h += '<div style="margin-top:8px;"><label style="font-size:12px;opacity:.8;">补充与新设定：</label><textarea id="step4Input" rows="2" placeholder="例：贴身仿写，保留核心公式..."></textarea></div><button class="btn primary full" onclick="cS4()" style="margin-top:10px;position:sticky;bottom:0;z-index:5;">确认方案，生成Step5&6</button></div>';
          s4.innerHTML = h; return;
        }
      }
      s4.style.display = 'none';

      // 3. Step 7 面板
      if (S.mode === '短剧对标' && S.s4 && !S.s7) {
        var la = CC().msgs.slice().reverse().find(function (m) { return m.role === 'assistant' && !m.er; });
        if (la && la.content.indexOf('"step":"step7_format"') !== -1) {
          s7.style.display = 'block';
          s7.innerHTML = '<div class="panel"><h4>📐 剧本格式确认</h4><details style="margin-bottom:6px;"><summary style="cursor:pointer;font-size:12px;">默认格式参考</summary><pre style="font-size:11px;background:var(--bg2);padding:8px;border-radius:6px;">集数：第X集   场次：X-Y   场景：简洁\n▲画面描述：简短动作表情\n角色A：台词\n【本集钩子】</pre></details><textarea id="step7Input" rows="3" placeholder="留空=使用默认格式"></textarea><button class="btn primary" onclick="cS7()" style="margin-top:6px;">确认，生成剧本</button></div>';
          return;
        }
      }
      s7.style.display = 'none';

      // 4. 批量生成面板
      if (S.mode === '短剧对标' && S.s7 && S.bi > 0) {
        bp.style.display = 'block';
        bp.innerHTML = '<div class="panel"><h4>📦 第' + S.bi + '轮完成（共' + S.tb + '轮）</h4>' + (S.bi < S.tb ? '<button class="btn primary" onclick="nB()" style="margin-top:6px;">继续第' + (S.bi + 1) + '轮</button>' : '') + '</div>';
        return;
      }
      bp.style.display = 'none';
    }

    function confirmCreateQA() {
      var sel = [];
      var data = tryParseS4();
      if (data) {
        var qs = data.step4_questions || data.questions;
        if (qs && qs.length) {
          for (var qi = 0; qi < qs.length; qi++) {
            var rad = document.querySelector('input[name="cq_' + qi + '"]:checked');
            if (rad) {
              var val = rad.value;
              var customBox = E('q_custom_' + qi);
              if (customBox && customBox.style.display !== 'none' && customBox.value.trim()) {
                val = '自定义：' + customBox.value.trim();
              }
              sel.push('Q' + (qi + 1) + '确认: 「' + qs[qi].question + '」 ➔ 意向选择: 「' + val + '」');
            }
          }
        }
      }

      var chat = CC();
      if (chat.msgs && chat.msgs.length) {
        for (var i = chat.msgs.length - 1; i >= 0; i--) {
          if (chat.msgs[i].role === 'assistant') {
            chat.msgs[i].handled = true;
            break;
          }
        }
      }

      S.step4Questions = null;
      chat.step4Questions = null;
      sv();

      var cp = E('createPanel');
      if (cp) { cp.style.display = 'none'; cp.innerHTML = ''; }

      var msgText = '## 确认选项\n' + (sel.join('\n') || '按最优创作方案执行');
      E('chatInput').value = msgText;
      sendMsg();
    }

    function pickCreateCard(st) {
      S.createStage = st;
      S.cardsVisible = false;
      sv();
      E('chatInput').value = '请继续执行剧本创作【' + st + '】。';
      sendMsg();
    }

    function cS4() {
      var sel = [];
      var data = tryParseS4();
      if (data) {
        var qs = data.step4_questions || data.questions;
        if (qs && qs.length) {
          for (var qi = 0; qi < qs.length; qi++) {
            var rad = document.querySelector('input[name="q_' + qi + '"]:checked');
            if (rad) {
              var val = rad.value;
              var customBox = E('q_custom_' + qi);
              if (customBox && customBox.style.display !== 'none' && customBox.value.trim()) {
                val = '自定义：' + customBox.value.trim();
              }
              sel.push(qs[qi].question + ' => ' + val);
            }
          }
        }
      }
      var v = E('step4Input').value.trim();
      if (v) sel.push('补充设定：' + v);
      S.s4 = true; sv();
      E('step4Panel').style.display = 'none';
      advanceBenchStep(5);
      E('chatInput').value = sel.length ? '以下是我选择的仿写方案：\n' + sel.join('\n') + '\n\n请基于此执行Step5和Step6。' : '贴身仿写，保留原剧核心公式。请执行Step5和Step6。';
      sendMsg();
    }

    function cS7() {
      var v = E('step7Input').value.trim();
      S.s7 = true; sv();
      E('step7Panel').style.display = 'none';
      advanceBenchStep(8);
      E('chatInput').value = '确认格式：' + (v || '使用默认格式') + '。请执行Step8，生成第1轮(第1-5集)。';
      sendMsg();
    }

    function nB() {
      var ns = S.bi * 5 + 1, ne = Math.min(ns + 4, S.tb * 5);
      E('chatInput').value = '执行Step8第' + (S.bi + 1) + '轮(第' + ns + '-' + ne + '集)，先做回顾。';
      S.bi += 1; sv();
      E('batchPanel').style.display = 'none';
      sendMsg();
    }

    // ====== 模式切换 ======
    function toggleMode(m) {
      svs();
      if (S.mode === m) {
        S.mode = null; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.benchStep = 1;
      } else {
        S.mode = m; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.benchStep = 1;
      }
      sv(); rf();
    }

    // ====== 渲染 ======
    function rf() {
      var s = E('themeSelect');
      s.innerHTML = Object.keys(TH).map(function (t) { return '<option>' + t + '</option>'; }).join('');
      s.value = localStorage.getItem('theme') || '🍑 蜜桃乌龙';
      switchTheme(s.value);

      var bB = E('btnBench'), bC = E('btnCreate');
      bB.textContent = '对标' + (S.mode === '短剧对标' ? ' ✓' : '');
      bC.textContent = '创作' + (S.mode === '剧本创作' ? ' ✓' : '');
      bB.className = 'btn' + (S.mode === '短剧对标' ? ' primary' : '');
      bC.className = 'btn' + (S.mode === '剧本创作' ? ' primary' : '');

      var ms = JSON.parse(localStorage.getItem('fm') || '["deepseek-chat","deepseek-reasoner","gpt-4o","gpt-4o-mini"]');
      E('modelSelect').innerHTML = ms.map(function (m) { return '<option value="' + m + '">' + m + '</option>'; }).join('');

      E('genStatus').innerHTML = '';
      rd();
      renderBenchSteps();
      listFiles();
      lds();
      renderHistory();
      E('chatInput').placeholder = '在【' + (S.mode || '通用') + '】模式下输入指令...';
    }

    function renderMarkdown(text) {
      if (!text) return '';
      var s = esc(text);

      s = s.replace(/\r\n/g, '\n');
      s = s.replace(/\n{3,}/g, '\n\n');

      s = s.replace(/```([\s\S]*?)```/g, function(match, code) {
        return '<pre style="background:#f8fafc;padding:10px 12px;border-radius:8px;border:1px solid #e2e8f0;font-family:monospace;font-size:12px;overflow-x:auto;margin:6px 0;white-space:pre-wrap;"><code>' + code + '</code></pre>';
      });

      s = s.replace(/^#### (.*$)/gim, '<h5 style="font-size:13px;font-weight:700;margin:8px 0 4px 0;color:#1e293b;">$1</h5>');
      s = s.replace(/^### (.*$)/gim, '<h4 style="font-size:14px;font-weight:700;margin:10px 0 4px 0;color:#2563eb;">$1</h4>');
      s = s.replace(/^## (.*$)/gim, '<h3 style="font-size:15px;font-weight:700;margin:12px 0 4px 0;color:#1e293b;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">$1</h3>');
      s = s.replace(/^# (.*$)/gim, '<h2 style="font-size:16px;font-weight:700;margin:14px 0 6px 0;color:#2563eb;">$1</h2>');

      s = s.replace(/^---$/gim, '<hr style="border:none;border-top:1px solid #e2e8f0;margin:8px 0;">');

      s = s.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#0f172a;font-weight:700;background:rgba(59,130,246,0.1);padding:1px 4px;border-radius:4px;margin:0 2px;">$1</strong>');

      s = s.replace(/\*(.*?)\*/g, '<em style="color:#475569;">$1</em>');

      s = s.replace(/^\s*[\-\*]\s+(.*$)/gim, '<div style="margin-left:12px;position:relative;padding-left:12px;margin:2px 0;"><span style="position:absolute;left:0;color:#3b82f6;">•</span>$1</div>');

      s = s.replace(/\n/g, '<br>');

      s = s.replace(/(?:<br>\s*){3,}/gi, '<br><br>');
      s = s.replace(/(<\/h[2-5]>|<hr>|<\/pre>)\s*<br>/gi, '$1');
      s = s.replace(/<br>\s*(<h[2-5]>|<hr>|<pre)/gi, '$1');

      return s.trim();
    }

    function rd() {
      var chat = CC(), area = E('chatArea'), h = '', msgs = chat.msgs;
      if (!msgs || !msgs.length) {
        h += '<div style="margin-bottom:12px;background:#dcfce7;border:1px solid #86efac;color:#166534;padding:8px 14px;border-radius:10px;font-size:12px;font-weight:600;display:flex;align-items:center;justify-content:space-between;"><span>✨ 当前已处于全新空白对话 (ID: ' + esc(S.cid) + ')</span><button class="btn xs" onclick="newChat()">清空重置</button></div>';
        if (S.mode === '短剧对标') {
          h += renderBenchGuide();
        } else if (S.mode === '剧本创作') {
          h += '<div class="guide-msg"><div class="guide-title">🎨 剧本创作模式 · 智能分析与追问体验</div><p>请在下方聊天框直接输入你的创作想法或概述（如："我想写一部女扮男装的宫廷追女爽剧..."），发送后 AI 将深入分析并向你提出定向选项卡片供你确认方案。</p></div>';
        } else {
          h += '<div style="text-align:center;padding:60px 0;opacity:.4;font-size:14px;">👆 点击底部「对标」或「创作」开始或在输入框中自由对话 ✨</div>';
        }
        
      if (S.multiSelectMode) {
        var selCount = Object.keys(S.selectedMsgs).filter(function(k){return S.selectedMsgs[k];}).length;
        h += '<div class="batch-bar"><span style="font-size:12px;font-weight:600">已选 ' + selCount + ' 条</span><button class="btn sm danger" onclick="deleteSelectedMsgs()">删除</button><button class="btn sm" onclick="toggleMultiSelect()">取消</button></div>';
      }
      area.innerHTML = h;
        return;
      }

      // 🔴 方案 1 性能优化：消息超过 15 条时，开启 UI 视口切片渲染（不影响文件资产存盘与后端全量保存）
      var batchBtn = '';
      if (!S.multiSelectMode && msgs.length > 0) {
        batchBtn = '<div style="text-align:right; margin-bottom:10px;"><button class="btn xs" onclick="toggleMultiSelect()">批量管理</button></div>';
      }
      h += batchBtn;
      var maxVisible = S.showAllMsgs ? msgs.length : 15;
      var startIdx = Math.max(0, msgs.length - maxVisible);

      if (startIdx > 0) {
        var hiddenCount = startIdx;
        h += '<div style="text-align:center;margin:6px 0 12px 0;"><button class="btn xs" onclick="S.showAllMsgs=true;rd();" style="background:var(--bg2);border:1px solid var(--border);color:var(--primary);font-weight:600;padding:6px 14px;border-radius:20px;">📜 已折叠更早的 ' + hiddenCount + ' 条历史消息 (点击加载全部对话)</button></div>';
      } else if (S.showAllMsgs && msgs.length > 15) {
        h += '<div style="text-align:center;margin:6px 0 12px 0;"><button class="btn xs" onclick="S.showAllMsgs=false;rd();" style="opacity:.6;padding:4px 10px;border-radius:14px;">收起更早消息</button></div>';
      }

      for (var i = startIdx; i < msgs.length; i++) {
        var m = msgs[i];
        if (!S.selectedMsgs) S.selectedMsgs = {};
        h += '<div class="msg-wrap ' + (m.role === 'user' ? 'is-user ' : '') + (S.multiSelectMode ? 'multi-select' : '') + '">';
        if (S.multiSelectMode) {
          h += '<input type="checkbox" class="msg-checkbox" ' + (S.selectedMsgs[i] ? 'checked' : '') + ' onclick="toggleSelectMsg(' + i + ')">';
        }
        if (m.role === 'user') {
          if (S.edi === i) {
            h += '<div class="msg user"><div class="role" style="display:flex;justify-content:flex-end;margin-bottom:4px;font-size:12px;opacity:0.6;">编辑中...</div><textarea class="edit-textarea" id="editArea" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);">' + esc(m.content) + '</textarea><div class="actions" style="margin-top:4px;display:flex;justify-content:flex-end;gap:8px;"><button class="btn sm primary" onclick="cfEd(' + i + ')">确认</button><button class="btn sm" onclick="S.edi=null;rd()">取消</button></div></div>';
          } else {
            h += '<div class="msg user"><div class="role" style="display:flex;justify-content:flex-end;margin-bottom:4px;"><button class="btn xs" onclick="S.edi=' + i + ';rd()" style="opacity:.4">✏️修改</button></div><div class="content">' + renderMarkdown(m.content) + '</div></div>';
          }
          h += '</div>'; // close msg-wrap
          continue;
        }
        if (m.er) {
          h += '<div class="err-box"><div style="font-weight:600;margin-bottom:4px;">生成失败</div><div>' + esc(m.content) + '</div>';
          if (i === msgs.length - 1 && !S.gen) h += '<div style="margin-top:6px;"><button class="btn sm" onclick="rgn(' + i + ')">重新生成</button></div>';
          h += '</div>';
          h += '</div>'; // close msg-wrap
          continue;
        }

        var rawContent = m.content || '';
        var disp = rawContent;
        if (S.mode === '剧本创作') {
          disp = disp.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, '');
        } else {
          disp = disp.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, '<span style="font-size:11px;opacity:.6;background:var(--bg);padding:1px 6px;border-radius:4px;display:inline-block;margin:2px 0;">📋 (模板数据已解析)</span>');
        }

        var thR = /<(?:think|thinking|thought)>([\s\S]*?)(?:<\/(?:think|thinking|thought)>|$)/gi, thH = '', tm;
        while ((tm = thR.exec(disp)) !== null) {
          if (tm[1]) thH += tm[1] + '\n';
        }
        disp = disp.replace(/<(?:think|thinking|thought)>[\s\S]*?(?:<\/(?:think|thinking|thought)>|$)/gi, '').trim();

        var isGenerating = m.s || (S.gen && i === msgs.length - 1);

        h += '<div class="msg assistant"><div class="role">🤖 助手</div>';
        if (thH.trim()) h += '<details class="think-box"><summary>🧠 思考过程 (点击展开/折叠)</summary><div style="margin-top:6px;opacity:.95;">' + renderMarkdown(thH.trim()) + '</div></details>';
        if (isGenerating) h += '<div class="think-box">🤔 AI 正在思考中<div class="dots"><span></span><span></span><span></span></div></div>';
        h += '<div class="content" id="msg_' + (m.id || '') + '">' + renderMarkdown(disp) + '</div>';

        if (i === msgs.length - 1 && !m.s && !S.gen) {
          h += '<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap;">';
          h += '<button class="btn sm" onclick="rgn(' + i + ')">重新生成</button>';
          if (S.mode === '短剧对标' && S.benchStep <= 8) {
            var nextPrompt = STEP_PROMPTS[S.benchStep];
            if (nextPrompt) {
              h += '<button class="btn sm primary" onclick="E(\'chatInput\').value=\'' + esc(nextPrompt).replace(/'/g, "\\'") + '\';E(\'chatInput\').focus();">继续步骤' + S.benchStep + ' →</button>';
            }
          }
          h += '</div>';
        }
        h += '</div>'; // close msg assistant
        h += '</div>'; // close msg-wrap
      }
      
      if (S.multiSelectMode) {
        var selCount = Object.keys(S.selectedMsgs).filter(function(k){return S.selectedMsgs[k];}).length;
        h += '<div class="batch-bar"><span style="font-size:12px;font-weight:600">已选 ' + selCount + ' 条</span><button class="btn sm danger" onclick="deleteSelectedMsgs()">删除</button><button class="btn sm" onclick="toggleMultiSelect()">取消</button></div>';
      }
      area.innerHTML = h;
      area.scrollTop = area.scrollHeight;
      rP();
    }

    function renderBenchGuide() {
      var h = '<div class="guide-msg">';
      h += '<div class="guide-title">🔬 短剧对标模式 · 8步流程</div>';
      h += '<p style="margin-bottom:8px;">此模式将引导你完成：上传参考剧本 → 拆解分析 → 提取模板 → 仿写方案 → 生成仿写剧本。</p>';
      h += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;font-size:12px;">';
      for (var i = 0; i < BENCH_STEPS.length; i++) {
        var s = BENCH_STEPS[i], isCurrent = (s.id === S.benchStep);
        h += '<div style="padding:4px 0;' + (isCurrent ? 'color:var(--primary);font-weight:700;' : 'opacity:.7;') + '">' + (isCurrent ? '👉 ' : '') + s.icon + ' Step' + s.id + ': ' + s.label + '</div>';
      }
      h += '</div>';
      h += '<div style="margin-top:10px;padding-top:8px;border-top:1px solid #e5e7eb;">';
      h += '<span style="font-weight:600;">📍 当前：Step ' + S.benchStep + ' - ' + BENCH_STEPS[S.benchStep - 1].label + '</span> ';
      h += '<span style="font-size:12px;opacity:.7;">— ' + getStepTip(S.benchStep) + '</span>';
      h += '<div class="preset-btns">';
      if (S.benchStep === 1) {
        h += '<span class="preset-btn" onclick="E(\'fileInput\').click()">📁 上传参考剧本</span>';
        h += '<span class="preset-btn" onclick="E(\'chatInput\').value=\'请帮我对标分析我上传的参考剧本，先确认已收到并阅读完毕。\';E(\'chatInput\').focus();">📤 已上传，开始分析</span>';
      } else {
        var p = STEP_PROMPTS[S.benchStep];
        if (p) h += '<span class="preset-btn" onclick="E(\'chatInput\').value=\'' + esc(p).replace(/'/g, "\\'") + '\';E(\'chatInput\').focus();">🚀 执行 Step ' + S.benchStep + '</span>';
      }
      h += '</div></div></div>';
      return h;
    }

    function rgn(idx) {
      var c = CC();
      c.msgs = c.msgs.slice(0, idx);
      sv(); rd();
      sendMsg(true);
    }

    // ====== 发送消息与 done 强制检测逻辑 ======
    async function sendMsg(isRegen) {
      if (typeof isRegen !== 'boolean') isRegen = false;
      var inp = E('chatInput'), txt = inp.value.trim();
      
      var chat = CC();
      var lastM = chat.msgs && chat.msgs.length ? chat.msgs[chat.msgs.length - 1] : null;
      if (S.gen && (!lastM || !lastM.s)) {
        S.gen = false;
      }

      if ((!txt && !isRegen) || S.gen) return;

      if (S.mode === '剧本创作') {
        S.cardsVisible = false;
        chat.cardsVisible = false;
      }

      if (!isRegen) inp.value = '';
      var k = gK(); if (!k) { alert('请先填写API Key'); return; }

      if (!isRegen && txt) {
        if (!chat.msgs.length || chat.msgs[chat.msgs.length - 1].content !== txt) chat.msgs.push({ role: 'user', content: txt });
      }
      sv(); rd();

      var docT = '';
      if (S.doc && (S.mode === '短剧对标' || S.mode === '剧本创作') && chat.msgs.filter(function (m) { return m.role === 'user'; }).length <= 2) {
        docT = S.doc;
      }

      if (S.mode === '短剧对标') {
        if (S.benchStep === 1 && txt.indexOf('已上传') !== -1) advanceBenchStep(2);
        else if (S.benchStep === 2 && (txt.indexOf('拆解') !== -1 || txt.indexOf('拉片') !== -1)) advanceBenchStep(3);
      }

      S.gen = true; S.ab = new AbortController();
      E('genStatus').innerHTML = '<button class="btn danger" onclick="stopGen()">⏹ 停止生成</button>';
      E('chatInput').disabled = true;

      var pid = 'm' + Date.now();
      chat.msgs.push({ role: 'assistant', content: '', s: true, id: pid });
      rd();

      try {
        var r = await fetch(B + '/api/chat', {
          method: 'POST',
          headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()),
          body: JSON.stringify({
            api_key: k, api_url: gU(), model: gM(), work_mode: S.mode || '通用',
            messages: chat.msgs.filter(function (m) { return !m.s; }).map(function (m) { return { role: m.role, content: m.content }; }),
            user_input: txt, doc_text: docT, session_id: S.cid, token: getToken()
          }),
          signal: S.ab.signal
        });

        var reader = r.body.getReader(), dec = new TextDecoder(), buf = '', full = '';
        while (true) {
          var rdv = await reader.read(); if (rdv.done) break;
          buf += dec.decode(rdv.value, { stream: true });
          var lines = buf.split('\n'); buf = lines.pop() || '';
          for (var li = 0; li < lines.length; li++) {
            var l = lines[li]; if (!l.startsWith('data: ')) continue;
            try {
              var d = JSON.parse(l.slice(6));
              if (d.token) {
                full += d.token;
                var m = chat.msgs.find(function (x) { return x.id === pid; });
                if (m) m.content = full;
                var el = E("msg_" + pid);
                if (el) {
                  el.innerHTML = renderMarkdown(full.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, ""));
                  let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 150;
                  if(isAtB2) E("chatArea").scrollTop = E("chatArea").scrollHeight;
                  rP();
                } else {
                  rd();
                }
              } else if (d.type === 'done') {
                var m = chat.msgs.find(function (x) { return x.id === pid; });
                if (m) { delete m.s; delete m.id; m.content = full; if (d.saved_file) m.content += '\n\n---\n📁 已保存: ' + d.saved_file; }

                var sdir = d.session_dir || d.sessiondir;
                if (sdir) S.sd = sdir;

                if (S.mode === '短剧对标' && S.benchStep === 3) {
                  advanceBenchStep(4);
                  S.s4 = false;
                }

                S.step4Questions = null;
                if (d.template_json) {
                  S.step4Questions = d.template_json;
                  var curC = CC();
                  curC.step4Questions = d.template_json;
                  var s = d.template_json.step;
                  if (s === 'step4_ready') S.s4 = false;
                  else if (s === 'step7_format') S.s7 = false;
                  else if (s === 'batch_complete') { S.bi = d.template_json.batch_index || 1; S.tb = d.template_json.total_batches || 0; }
                }

                var dyn = tryParseS4();
                if (dyn && (dyn.step === 'step4_ready' || dyn.step4_questions || dyn.questions)) {
                  if (S.mode === '短剧对标') {
                    S.s4 = false;
                    advanceBenchStep(4);
                  }
                }

                sv(); rd(); listFiles();
              } else if (d.type === 'error') {
                var m = chat.msgs.find(function (x) { return x.id === pid; });
                if (m) { m.content = d.message; m.er = true; delete m.s; delete m.id; }
                rd();
              }
            } catch (e) { }
          }
        }
      } catch (e) {
        var m = chat.msgs.find(function (x) { return x.id === pid; });
        if (e.name !== 'AbortError') {
          if (m) { m.content = '请求失败：' + e.message; m.er = true; delete m.s; delete m.id; }
        } else {
          if (m) { m.content += '\n\n[用户停止了生成]'; delete m.s; delete m.id; }
        }
      }

      S.gen = false; S.ab = null;
      E('genStatus').innerHTML = ''; E('chatInput').disabled = false; E('chatInput').focus();
      rd(); sv();
    }

    function stopGen() { if (S.ab) S.ab.abort(); }
    function cfEd(idx) {
      var c = CC(), nv = E('editArea').value.trim();
      if (nv) { c.msgs[idx].content = nv; c.msgs = c.msgs.slice(0, idx + 1); }
      S.edi = null; sv(); rd();
    }

    // ====== 文件操作与删除 ======
    function clearDoc() {
      S.doc = '';
      var inp = E('fileInput'); if (inp) inp.value = '';
      E('fileInfo').innerHTML = '未选择文件';
      showToast('🗑️ 参考脚本已成功清除！');
    }

    async function handleFileUpload(inp) {
      var files = inp.files;
      if (!files || !files.length) return;
      S.doc = '';
      var texts = [], infos = [];
      E('fileInfo').innerHTML = '⏳ 正在解析 ' + files.length + ' 个文件...';
      for (var i = 0; i < files.length; i++) {
        var f = files[i];
        var fd = new FormData();
        fd.append('file', f);
        try {
          var r = await fetch(B + '/api/upload', { method: 'POST', body: fd });
          var d = await r.json();
          if (d.text) {
            texts.push('【文件' + (i + 1) + ': ' + d.filename + '】\n' + d.text);
            infos.push(d.filename + '（' + d.word_count + '字）');
          }
        } catch (e) { }
      }
      if (texts.length) {
        S.doc = texts.join('\n\n---\n\n');
        E('fileInfo').innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px;"><span>✅ 已成功合并上传 ' + texts.length + ' 个文件</span><button class="btn xs danger" onclick="clearDoc()">🗑️ 清除</button></div><div style="font-size:11px;opacity:.7;margin-top:2px;">' + infos.join('<br>') + '</div>';
        if (S.mode === '短剧对标') advanceBenchStep(2);
      } else {
        E('fileInfo').innerHTML = '<span style="color:#ff6b6b">上传失败</span>';
      }
    }

    async function listFiles() {
      if (!S.sd) S.sd = 'session_' + S.cid;
      var sid = S.sd.replace(/\\/g, '/').split('/').pop();
      try {
        var r = await fetch(B + '/api/files/' + sid + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() }), d = await r.json();
        if (d.files && d.files.length) {
          E('projectFiles').innerHTML = d.files.map(function (f) {
            return '<div style="margin:4px 0;display:flex;justify-content:space-between;align-items:center;background:var(--bg);padding:4px 8px;border-radius:6px;border:1px solid var(--border);">' +
              '<span style="cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px;" onclick="pv(\'' + f.path + '\')" title="' + esc(f.name) + '">📄 ' + esc(f.name) + '</span>' +
              '<div style="display:flex;gap:4px;">' +
              '<a href="' + B + '/api/download/' + f.path + '" download class="btn xs" style="text-decoration:none" title="下载">⬇</a>' +
              '<button class="btn xs danger" onclick="delFile(\'' + f.path + '\')" title="物理删除文件">🗑️</button>' +
              '</div></div>';
          }).join('');
        } else E('projectFiles').innerHTML = '暂无';
      } catch (e) { E('projectFiles').innerHTML = '暂无'; }
    }

    async function delFile(path) {
      if (!confirm('确定要物理删除该文件吗？')) return;
      try {
        var r = await fetch(B + '/api/delete/' + path + '?token=' + encodeURIComponent(getToken()), { method: 'DELETE', headers: getAuthHeaders() });
        var d = await r.json();
        if (d.status === 'ok') {
          showToast('🗑️ 文件已成功删除！');
          E('previewBox').style.display = 'none';
          listFiles();
        } else {
          alert('删除失败：' + (d.error || '未知错误'));
        }
      } catch (e) {
        alert('删除请求失败：' + e.message);
      }
    }

    async function pv(path) {
      try {
        
        E('editorFileName').innerText = '加载中...';
          E('editorContent').contentEditable = 'true';
        E('editorContent').innerText = '正在读取文件内容，请稍候...';
        E('editorSaveStatus').innerText = '';
        currentPreviewFile = path;

        var t = '';
        try {
          var r = await fetch(B + '/api/preview/' + path + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() });
          if (r.ok) {
            var d = await r.json();
            t = d.text || d.error || '';
          } else {
            var r2 = await fetch(B + '/api/download/' + path);
            t = await r2.text();
          }
        } catch(netErr) {
          t = '网络请求失败，请检查服务器是否正常运行。' + netErr.message;
        }
        
        // 只有当用户没有切换到其他文件时才更新
        if (currentPreviewFile === path) {
          E('editorFileName').innerText = path.split('/').pop();
          E('editorContent').innerText = t;
          updateWordCount();
        }
      } catch (e) { 
        if (currentPreviewFile === path) {
          E('editorContent').innerText = '读取失败: ' + e.message;
        }
      }
    }

    async function fetchModels() {
      var k = gK(), u = gU();
      if (!k) { alert('请先填写API Key'); return; }
      try {
        var r = await fetch(B + '/api/fetch-models', { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()), body: JSON.stringify({ api_key: k, api_url: u }) });
        var d = await r.json();
        if (d.models && d.models.length) {
          E('modelSelect').innerHTML = d.models.map(function (m) { return '<option value="' + m + '">' + m + '</option>'; }).join('');
          localStorage.setItem('fm', JSON.stringify(d.models));
          svs();
          E('apiStatus').className = 'status-tag ok'; E('apiStatus').innerHTML = '🟢 已连接(' + d.models.length + ')';
          alert('拉取成功：' + d.models.length + '个模型');
        } else alert('拉取失败：' + (d.error || '无模型返回'));
      } catch (e) { alert('拉取失败：' + e.message); }
    }

    
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
        // openAuthModal();
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
          headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()),
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
          
          // 将所有远程的 session 注入到 S.chats 里，这样 renderHistorySelect 才能渲染它们
          d.sessions.forEach(function(s) {
            var exists = S.chats.find(function(c) { return c.id === s.session_id; });
            if (!exists) {
              S.chats.push({ id: s.session_id, title: s.title, msgs: [], sd: null, mode: s.mode, benchStep: 1, step4Questions: null, cstr: false, qaHandled: false, cardsVisible: true });
            }
          });
          
          var sel = document.getElementById('historySelect');
          if (sel) {
            // ...
            sel.innerHTML = S.chats.map(function(c) {
              return '<option value="' + c.id + '">' + esc(c.title || '对话') + '</option>';
            }).join('');
            
            sel.value = S.cid;
            if (sel.value !== S.cid) {
               sel.value = d.sessions[0].session_id;
            }
            try {
              var cidToFetch = sel.value || S.cid;
              var r2 = await fetch(B + '/api/history/detail/' + cidToFetch + '?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
              var d2 = await r2.json();
              if (d2.status === 'ok' && d2.messages) {
                S.cid = cidToFetch;
                var targetC = CC();
                targetC.msgs = d2.messages;
                sv(); rf();
              }
            } catch(e) {}
          }
        }
      } catch(e) {}
    }

    function exportHistory() {
      if (!S.chats || S.chats.length === 0) {
        alert("没有可导出的历史记录");
        return;
      }
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(S.chats, null, 2));
      var downloadAnchorNode = document.createElement('a');
      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", "history_backup.json");
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    }

    async function importHistory(event) {
      var file = event.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = async function(e) {
        try {
          var importedChats = JSON.parse(e.target.result);
          if (!Array.isArray(importedChats)) {
            alert("导入的文件格式不正确！");
            return;
          }
          if (!S.chats) S.chats = [];
          
          var newCount = 0;
          importedChats.forEach(function(ic) {
            var exists = S.chats.find(function(c) { return c.id === ic.id; });
            if (!exists) {
              S.chats.push(ic);
              newCount++;
            }
          });
          
          sv();
          rf();
          
          if (newCount > 0) {
            alert("成功导入了 " + newCount + " 条新记录。正在自动同步到云端...");
            var token = getToken();
            if (token) {
              try {
                var res = await fetch(B + '/api/history/sync', {
                  method: 'POST',
                  headers: Object.assign({'Content-Type': 'application/json'}, getAuthHeaders()),
                  body: JSON.stringify({
                    token: token,
                    chats: importedChats
                  })
                });
                var d = await res.json();
                if (d.status === 'ok') {
                  alert("云端同步完成！成功同步了 " + d.synced_count + " 条记录。");
                  loadUserHistorySessions(); // 刷新云端列表
                } else {
                  alert("云端同步失败: " + d.message);
                }
              } catch(err) {
                alert("云端同步请求出错，请确保你已登录并且网络畅通。");
              }
            } else {
              alert("导入成功，但你未登录账号，无法同步到云端。");
            }
          } else {
            alert("没有发现新的记录，所有记录已存在。");
          }
        } catch(err) {
          alert("解析备份文件失败: " + err.message);
        }
        document.getElementById('importFile').value = "";
      };
      reader.readAsText(file);
    }

    ld(); lds(); rf(); checkAuthStatus();
  
    // Quote feature
    document.addEventListener('mouseup', function(e) {
      if(e.target.id === 'quoteBtn') return;
      setTimeout(() => {
        let sel = window.getSelection();
        let text = sel.toString().trim();
        let btn = document.getElementById('quoteBtn');
        if (!text) {
            btn.style.display = 'none';
            return;
        }
        let rect = sel.getRangeAt(0).getBoundingClientRect();
        btn.style.display = 'block';
        btn.style.left = Math.max(10, rect.left + (rect.width / 2) - 35) + 'px';
        btn.style.top = Math.max(10, rect.top - 40) + 'px';
      }, 10);
    });
    document.addEventListener('mousedown', function(e) {
      if(e.target.id !== 'quoteBtn') {
          let btn = document.getElementById('quoteBtn');
          if(btn) btn.style.display = 'none';
      }
    });
    function handleQuote() {
      let sel = window.getSelection();
      let text = sel.toString().trim();
      if(text) {
          let input = document.getElementById('chatInput');
          let existing = input.value;
          input.value = '> ' + text + '\n\n' + existing;
          input.focus();
          document.getElementById('quoteBtn').style.display = 'none';
          window.getSelection().removeAllRanges();
          
          window.pendingQuoteContext = {
              text: text,
              file: window.currentPreviewFile || null
          };
      }
    }
    
  
    async function applySmartPatch(msgId, ctxStr) {
        var ctx = JSON.parse(decodeURIComponent(ctxStr));
        var c = S.chats.find(function(x) { return x.id === S.cid; });
        var m = c.msgs.find(function(x) { return x.id === msgId; });
        if (!m) return;
        
        var newText = m.content.trim();
        var oldText = ctx.text;
        var file = ctx.file;
        
        if (window.currentPreviewFile !== file) {
            await pv(file);
            // wait for render
            await new Promise(r => setTimeout(r, 500));
        }
        
        var editor = document.getElementById('editorContent');
        var currentContent = editor.innerText;
        
        if (currentContent.indexOf(oldText) === -1) {
            // Try stripping leading/trailing whitespace which might have been altered
            var strippedOld = oldText.replace(/^\s+|\s+$/g, '');
            if (currentContent.indexOf(strippedOld) !== -1) {
                oldText = strippedOld;
            } else {
                alert("在文档中找不到原始引用的文本，可能已经被手动修改过了。");
                return;
            }
        }
        
        var updatedContent = currentContent.replace(oldText, newText);
        editor.innerText = updatedContent;
        
        await saveEditorContent();
        
        removeSmartPatch(msgId);
        
        // Show success animation or alert
        var btn = document.getElementById('btnCreate');
        var oldBtnText = btn ? btn.innerText : '';
        if(btn) {
            btn.innerText = '✅ 覆写成功！';
            setTimeout(() => btn.innerText = oldBtnText, 2000);
        } else {
            alert("✅ 覆写成功并已保存！");
        }
    }

    function removeSmartPatch(msgId) {
        var c = S.chats.find(function(x) { return x.id === S.cid; });
        var m = c.msgs.find(function(x) { return x.id === msgId; });
        if (m) {
            delete m.quoteContext;
            sv();
            rf();
        }
    }


    const resizer = document.getElementById('resizer');
    const sidebar = document.getElementById('sidebar');
    let isDragging = false;

    if (resizer && sidebar) {
        resizer.addEventListener('mousedown', function(e) {
          isDragging = true;
          resizer.classList.add('dragging');
          document.body.style.cursor = 'col-resize';
          document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', function(e) {
          if (!isDragging) return;
          let newWidth = e.clientX;
          if (newWidth < 180) newWidth = 180;
          if (newWidth > 600) newWidth = 600;
          sidebar.style.width = newWidth + 'px';
          sidebar.style.flexBasis = newWidth + 'px';
          sidebar.style.minWidth = newWidth + 'px';
          sidebar.style.maxWidth = newWidth + 'px';
        });

        document.addEventListener('mouseup', function(e) {
          if (isDragging) {
            isDragging = false;
            resizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
          }
        });
    }

