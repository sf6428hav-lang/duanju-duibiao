0001: 
0002:     var B = (window.location.origin === 'file://' || window.location.origin === 'null') ? 'http://localhost:8000' : window.location.origin;
0003:     var TH = {
0004:       "🍑 蜜桃乌龙": { bg: "#faf7f5", bg2: "#ffffff", text: "#332927", primary: "#e07a5f", card: "#ffffff", border: "#f0e6e1", shadow: "0 4px 16px rgba(224,122,95,0.08)", radius: "12px", eb: "#fdf2f2", ebd: "#f8b4b4", dot: "#e07a5f", stepDone: "#10b981", stepActive: "#e07a5f", stepPending: "#d1d5db" },
0005:       "🌿 薄荷暗色": { bg: "#1e2328", bg2: "#161a1e", text: "#d0d6d8", primary: "#68b893", card: "#262c32", border: "#353d45", shadow: "0 4px 20px rgba(0,0,0,0.25)", radius: "10px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#68b893", stepDone: "#34d399", stepActive: "#68b893", stepPending: "#4b5563" },
0006:       "🫐 蓝莓暗夜": { bg: "#1a1d2e", bg2: "#141726", text: "#c8cddb", primary: "#7c8ce0", card: "#232740", border: "#353b58", shadow: "0 4px 20px rgba(0,0,0,0.30)", radius: "10px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#7c8ce0", stepDone: "#34d399", stepActive: "#7c8ce0", stepPending: "#4b5563" },
0007:       "🖤 曜石极简": { bg: "#111111", bg2: "#0a0a0a", text: "#cccccc", primary: "#eeeeee", card: "#1a1a1a", border: "#333333", shadow: "0 4px 20px rgba(0,0,0,0.40)", radius: "4px", eb: "#3a1a1a", ebd: "#ff6b6b", dot: "#eeeeee", stepDone: "#22c55e", stepActive: "#eeeeee", stepPending: "#555555" },
0008:       "🍷 醉红香槟": { bg: "#fdfbf7", bg2: "#ffffff", text: "#2d2424", primary: "#c05621", card: "#ffffff", border: "#f3ebd9", shadow: "0 4px 16px rgba(192,86,33,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#c05621", stepDone: "#38a169", stepActive: "#c05621", stepPending: "#cbd5e0" },
0009:       "🌌 极光深空": { bg: "#0f172a", bg2: "#0b1120", text: "#e2e8f0", primary: "#38bdf8", card: "#1e293b", border: "#334155", shadow: "0 4px 20px rgba(0,0,0,0.35)", radius: "10px", eb: "#451a1a", ebd: "#f87171", dot: "#38bdf8", stepDone: "#34d399", stepActive: "#38bdf8", stepPending: "#64748b" },
0010:       "🍵 静心抹茶": { bg: "#f4f7f4", bg2: "#ffffff", text: "#243224", primary: "#48bb78", card: "#ffffff", border: "#e2ebe2", shadow: "0 4px 16px rgba(72,187,120,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#48bb78", stepDone: "#38a169", stepActive: "#48bb78", stepPending: "#cbd5e0" },
0011:       "🍊 焦糖琥珀": { bg: "#fefcf9", bg2: "#ffffff", text: "#3c2a1e", primary: "#dd6b20", card: "#ffffff", border: "#fbd5c0", shadow: "0 4px 16px rgba(221,107,32,0.08)", radius: "12px", eb: "#fff5f5", ebd: "#feb2b2", dot: "#dd6b20", stepDone: "#38a169", stepActive: "#dd6b20", stepPending: "#cbd5e0" },
0012:       "🌃 霓虹夜幕": { bg: "#13111c", bg2: "#0d0b14", text: "#dcd7ec", primary: "#a855f7", card: "#1c182b", border: "#2e2844", shadow: "0 4px 20px rgba(0,0,0,0.35)", radius: "10px", eb: "#3b1219", ebd: "#f43f5e", dot: "#a855f7", stepDone: "#10b981", stepActive: "#a855f7", stepPending: "#6b7280" },
0013:       "🩶 莫兰迪灰": { bg: "#f0f2f5", bg2: "#ffffff", text: "#2c3e50", primary: "#64748b", card: "#ffffff", border: "#cbd5e1", shadow: "0 4px 16px rgba(100,116,139,0.08)", radius: "8px", eb: "#fef2f2", ebd: "#fca5a5", dot: "#64748b", stepDone: "#10b981", stepActive: "#64748b", stepPending: "#94a3b8" }
0014:     };
0015: 
0016:     
0017:     let currentPreviewFile = "";
0018: 
0019:     function updateWordCount() {
0020:       var text = E('editorContent').innerText || "";
0021:       var count = text.replace(/\s/g, '').length;
0022:       E('editorWordCountStr').innerText = '字数：' + count;
0023:       E('editorSaveStatus').innerText = '未保存';
0024:       E('editorSaveStatus').style.color = '#ef4444';
0025:     }
0026: 
0027:     async function saveEditorContent() {
0028:       if(!currentPreviewFile) return;
0029:       var text = E('editorContent').innerText;
0030:       E('editorSaveStatus').innerText = '保存中...';
0031:       try {
0032:         var r = await fetch(B + '/api/save_file', {
0033:           method: 'POST',
0034:           headers: { 'Content-Type': 'application/json', 'Authorization': localStorage.getItem('sdt_token') || '' },
0035:           body: JSON.stringify({ filepath: currentPreviewFile, content: text })
0036:         });
0037:         var d = await r.json();
0038:         if (d.status === 'ok') {
0039:           E('editorSaveStatus').innerText = '已保存';
0040:           E('editorSaveStatus').style.color = '#10b981';
0041:           showToast('保存成功');
0042:         } else {
0043:           alert('保存失败: ' + d.error);
0044:         }
0045:       } catch(e) {
0046:         alert('保存失败: ' + e.message);
0047:       }
0048:     }
0049: 
0050:     function closeEditor() {
0051:       E('editorPane').style.display = 'none';
0052:       currentPreviewFile = "";
0053:     }
0054: 
0055:     // 对标流程 8 步定义
0056:     var BENCH_STEPS = [
0057:       { id: 1, icon: '📤', label: '上传参考' },
0058:       { id: 2, icon: '🔍', label: '拆解分析' },
0059:       { id: 3, icon: '📋', label: '提取模板' },
0060:       { id: 4, icon: '🎯', label: '仿写方案' },
0061:       { id: 5, icon: '📝', label: '生成大纲' },
0062:       { id: 6, icon: '✅', label: '大纲确认' },
0063:       { id: 7, icon: '📐', label: '格式确认' },
0064:       { id: 8, icon: '🎬', label: '生成剧本' }
0065:     ];
0066: 
0067:     // 每步的预设 prompt
0068:     var STEP_PROMPTS = {
0069:       1: '请帮我对标分析我上传的参考剧本，先确认已收到并阅读完毕。',
0070:       2: '请对参考剧本进行逐集拆解分析（拉片），提取每集的情节节拍、钩子设计、情绪曲线、节奏量化指标。',
0071:       3: '请基于拆解结果，提取可复用的结构模板，包括：剧情节拍公式、人物弧光模式、每集钩子位置与类型、付费留客悬念设计。',
0072:       4: null,
0073:       5: '请基于确认的仿写方案，生成仿写短剧的分集大纲。',
0074:       6: null,
0075:       7: null,
0076:       8: '请按照确认的格式，开始逐集生成完整剧本。'
0077:     };
0078: 
0079:     var S = { cid: 'c' + Date.now(), mode: null, chats: [], doc: '', s4: false, s7: false, cstr: false, qaHandled: false, cardsVisible: true, bi: 0, tb: 0, gen: false, ab: null, sd: null, edi: null, step4Questions: null, createStage: '头脑风暴', benchStep: 1 };
0080: 
0081:     function E(id) { return document.getElementById(id); }
0082:     function esc(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
0083: 
0084:     function showToast(msg) {
0085:       var t = document.createElement('div');
0086:       t.className = 'toast-msg';
0087:       t.innerText = msg;
0088:       document.body.appendChild(t);
0089:       setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 2000);
0090:     }
0091: 
0092:     function sv() {
0093:       var curC = CC();
0094:       curC.step4Questions = S.step4Questions;
0095:       curC.cstr = S.cstr;
0096:       curC.qaHandled = S.qaHandled;
0097:       curC.cardsVisible = (S.cardsVisible !== false);
0098:       localStorage.setItem('app', JSON.stringify({ v: 'v55', cid: S.cid, mode: S.mode, chats: S.chats, s4: S.s4, s7: S.s7, cstr: S.cstr, qaHandled: S.qaHandled, cardsVisible: S.cardsVisible, bi: S.bi, tb: S.tb, sd: S.sd, createStage: S.createStage, benchStep: S.benchStep }));
0099:     }
0100: 
0101:     function ld() {
0102:       try {
0103:         var raw = localStorage.getItem('app');
0104:         if (raw) {
0105:           var d = JSON.parse(raw);
0106:           if (d) {
0107:             S.cid = d.cid || S.cid; S.mode = d.mode; S.chats = d.chats || []; S.s4 = d.s4 || false; S.s7 = d.s7 || false; S.cstr = d.cstr || false; S.qaHandled = d.qaHandled || false; S.cardsVisible = (d.cardsVisible !== false); S.bi = d.bi || 0; S.tb = d.tb || 0; S.sd = d.sd; S.createStage = d.createStage || '头脑风暴'; S.benchStep = d.benchStep || 1;
0108:             var curC = S.chats.find(function(x){ return x.id === S.cid; });
0109:             S.step4Questions = curC ? (curC.step4Questions || null) : null;
0110:           }
0111:         }
0112:       } catch (e) { }
0113:     }
0114: 
0115:     function svs() {
0116:       var mVal = E('customModel').value.trim() || E('modelSelect').value;
0117:       localStorage.setItem('apis', JSON.stringify({ k: E('apiKey').value, u: E('apiUrl').value, m: mVal }));
0118:       updateApiStatus();
0119:     }
0120: 
0121:     function lds() {
0122:       try {
0123:         var d = JSON.parse(localStorage.getItem('apis'));
0124:         if (d) {
0125:           if (d.k !== undefined) E('apiKey').value = d.k;
0126:           if (d.u !== undefined) E('apiUrl').value = d.u || 'https://yunwu.ai/v1';
0127:           if (d.m) {
0128:             var opts = E('modelSelect').options, has = false;
0129:             for (var i = 0; i < opts.length; i++) {
0130:               if (opts[i].value === d.m) { E('modelSelect').value = d.m; has = true; break; }
0131:             }
0132:             if (!has) E('customModel').value = d.m;
0133:           }
0134:         }
0135:       } catch (e) { }
0136:       updateApiStatus();
0137:     }
0138: 
0139:     function updateApiStatus() {
0140:       var k = E('apiKey').value.trim(), st = E('apiStatus');
0141:       if (!k) { st.className = 'status-tag err'; st.innerHTML = '🔴 未设置Key'; }
0142:       else { st.className = 'status-tag ok'; st.innerHTML = '🟢 已准备'; }
0143:     }
0144: 
0145:     function gM() { return E('customModel').value.trim() || E('modelSelect').value || 'gpt-4o'; }
0146:     function gK() { return E('apiKey').value.trim(); }
0147:     function gU() { return E('apiUrl').value.trim() || 'https://yunwu.ai/v1'; }
0148: 
0149:     
0150:     function toggleMultiSelect() {
0151:       S.multiSelectMode = !S.multiSelectMode;
0152:       S.selectedMsgs = {};
0153:       rd();
0154:     }
0155:     
0156:     function toggleSelectMsg(idx) {
0157:       S.selectedMsgs[idx] = !S.selectedMsgs[idx];
0158:       rd();
0159:     }
0160:     
0161:     function deleteSelectedMsgs() {
0162:       var c = CC();
0163:       var toDelete = Object.keys(S.selectedMsgs).filter(function(k) { return S.selectedMsgs[k]; }).map(Number);
0164:       if (toDelete.length === 0) {
0165:         alert("请先选择要删除的消息");
0166:         return;
0167:       }
0168:       if (!confirm("确定要删除选中的 " + toDelete.length + " 条消息吗？删除后AI将丢失这段记忆。")) return;
0169:       
0170:       toDelete.sort(function(a,b) { return b - a; });
0171:       for (var i = 0; i < toDelete.length; i++) {
0172:         c.msgs.splice(toDelete[i], 1);
0173:       }
0174:       S.multiSelectMode = false;
0175:       S.selectedMsgs = {};
0176:       sv(); rd();
0177:     }
0178: 
0179:     function CC() {
0180:       if (!S.chats) S.chats = [];
0181:       var c = S.chats.find(function (x) { return x.id === S.cid; });
0182:       if (!c) {
0183:         c = { id: S.cid, title: '新对话', msgs: [], sd: null, mode: S.mode, benchStep: 1, step4Questions: null, cstr: false, qaHandled: false, cardsVisible: true };
0184:         S.chats.unshift(c);
0185:       }
0186:       return c;
0187:     }
0188: 
0189:     function cleanEmptyChats() {
0190:       if (!S.chats) return;
0191:       S.chats = S.chats.filter(function (c) {
0192:         return (c.id === S.cid) || (c.msgs && c.msgs.length > 0);
0193:       });
0194:     }
0195: 
0196:     function newChat() {
0197:       var curC = CC();
0198:       if (curC.msgs && curC.msgs.length) {
0199:         var f = curC.msgs.find(function (m) { return m.role === 'user'; });
0200:         curC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
0201:       }
0202:       curC.mode = S.mode; curC.sd = S.sd; curC.benchStep = S.benchStep; curC.s4 = S.s4; curC.s7 = S.s7; curC.step4Questions = S.step4Questions; curC.cstr = S.cstr; curC.qaHandled = S.qaHandled; curC.cardsVisible = S.cardsVisible;
0203: 
0204:       cleanEmptyChats();
0205: 
0206:       var newId = 'c' + Date.now();
0207:       var keepMode = S.mode;
0208: 
0209:       var newC = {
0210:         id: newId,
0211:         title: '新对话',
0212:         msgs: [],
0213:         sd: null,
0214:         mode: keepMode,
0215:         benchStep: 1,
0216:         s4: false,
0217:         s7: false,
0218:         cstr: false,
0219:         qaHandled: false,
0220:         cardsVisible: true,
0221:         step4Questions: null
0222:       };
0223: 
0224:       S.chats.unshift(newC);
0225:       S.cid = newId;
0226:       S.mode = keepMode; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.tb = 0; S.sd = null; S.step4Questions = null; S.benchStep = 1; S.gen = false;
0227: 
0228:       sv();
0229: 
0230:       var inp = E('chatInput'); if (inp) inp.value = '';
0231:       var area = E('chatArea'); if (area) area.innerHTML = '';
0232:       
0233:       ['createPanel', 'step4Panel', 'step7Panel', 'batchPanel'].forEach(function(id) {
0234:         var p = E(id);
0235:         if (p) { p.style.display = 'none'; p.innerHTML = ''; }
0236:       });
0237: 
0238:       rf();
0239:       showToast('✨ 已成功为您创建全新对话！');
0240:     }
0241: 
0242:     async function swChat(id) {
0243:       if (id === S.cid) return;
0244:       var curC = CC();
0245:       if (curC.msgs && curC.msgs.length) {
0246:         var f = curC.msgs.find(function (m) { return m.role === 'user'; });
0247:         curC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
0248:       }
0249:       curC.mode = S.mode; curC.sd = S.sd; curC.benchStep = S.benchStep; curC.s4 = S.s4; curC.s7 = S.s7; curC.step4Questions = S.step4Questions; curC.cstr = S.cstr; curC.qaHandled = S.qaHandled; curC.cardsVisible = S.cardsVisible;
0250:       
0251:       cleanEmptyChats();
0252:       sv();
0253: 
0254:       S.cid = id;
0255:       var targetC = CC();
0256: 
0257:       var token = getToken();
0258:       if (token) {
0259:         try {
0260:           var r = await fetch(B + '/api/history/detail/' + id + '?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
0261:           var d = await r.json();
0262:           if (d.status === 'ok' && d.messages) {
0263:             targetC.msgs = d.messages;
0264:             if (d.messages.length > 0) {
0265:               var f = d.messages.find(function (m) { return m.role === 'user'; });
0266:               targetC.title = f ? f.content.replace(/[#*\[\]【】\s]/g, '').slice(0, 14) : '对话';
0267:             }
0268:           }
0269:         } catch(e) {}
0270:       }
0271:       S.mode = targetC.mode || null;
0272:       S.sd = targetC.sd || null;
0273:       S.s4 = targetC.s4 || false;
0274:       S.s7 = targetC.s7 || false;
0275:       S.cstr = targetC.cstr || false;
0276:       S.qaHandled = targetC.qaHandled || false;
0277:       S.cardsVisible = (targetC.cardsVisible !== false);
0278:       S.bi = 0;
0279:       S.step4Questions = targetC.step4Questions || null;
0280:       S.benchStep = targetC.benchStep || 1;
0281:       S.gen = false;
0282: 
0283:       sv(); rf();
0284:     }
0285: 
0286:     function delChat(id) {
0287:       S.chats = S.chats.filter(function (c) { return c.id !== id; });
0288:       if (S.cid === id) {
0289:         cleanEmptyChats();
0290:         if (S.chats.length) swChat(S.chats[0].id);
0291:         else newChat();
0292:       } else { sv(); rf(); }
0293:     }
0294: 
0295:     function openHistory() { renderHistory(); E('historyModal').classList.add('open'); }
0296:     function closeHistory() { E('historyModal').classList.remove('open'); }
0297:     
0298:     function renderHistorySelect() {
0299:       var sel = E('historySelect');
0300:       if (!sel) return;
0301:       var list = S.chats || [];
0302:       var h = '';
0303:       for (var i = 0; i < list.length; i++) {
0304:         var c = list[i], t = c.title || '对话 ' + (i + 1), is = (c.id === S.cid);
0305:         h += '<option value="' + c.id + '" ' + (is ? 'selected' : '') + '>' + (is ? '👉 ' : '💬 ') + esc(t) + '</option>';
0306:       }
0307:       sel.innerHTML = h;
0308:       sel.value = S.cid;
0309:     }
0310: 
0311:     function renderHistory() {
0312:       renderHistorySelect();
0313:       var hl = E('historyModalList');
0314:       if (!hl) return;
0315:       var hc = '', list = S.chats || [];
0316:       for (var i = 0; i < list.length; i++) {
0317:         var c = list[i], t = c.title || '对话 ' + (i + 1), is = (c.id === S.cid), cnt = (c.msgs ? c.msgs.length : 0);
0318:         hc += '<div class="modal-item ' + (is ? 'active' : '') + '" onclick="swChat(\'' + c.id + '\');closeHistory();"><div style="flex:1"><div style="font-weight:600;font-size:13px;' + (is ? 'color:var(--primary)' : '') + '">' + (is ? '👉 ' : '💬 ') + esc(t) + '</div><div style="font-size:11px;opacity:.5;margin-top:2px;">' + cnt + ' 条对话</div></div><button class="btn xs" onclick="event.stopPropagation();delChat(\'' + c.id + '\');renderHistory();" style="opacity:.5;">✕</button></div>';
0319:       }
0320:       hl.innerHTML = hc || '<div style="text-align:center;padding:30px 0;opacity:.4;font-size:13px;">暂无历史对话记录</div>';
0321:     }
0322: 
0323:     function switchTheme(n) {
0324:       var t = TH[n], r = document.documentElement.style;
0325:       r.setProperty('--bg', t.bg); r.setProperty('--bg2', t.bg2); r.setProperty('--text', t.text);
0326:       r.setProperty('--primary', t.primary); r.setProperty('--card', t.card); r.setProperty('--border', t.border);
0327:       r.setProperty('--shadow', t.shadow); r.setProperty('--radius', t.radius); r.setProperty('--err-bg', t.eb);
0328:       r.setProperty('--err-border', t.ebd); r.setProperty('--dot', t.dot);
0329:       r.setProperty('--step-done', t.stepDone); r.setProperty('--step-active', t.stepActive); r.setProperty('--step-pending', t.stepPending);
0330:       localStorage.setItem('theme', n);
0331:     }
0332: 
0333:     // ====== 对标流程步骤条 ======
0334:     function renderBenchSteps() {
0335:       var bar = E('benchStepsBar'), inner = E('benchStepsInner');
0336:       if (S.mode !== '短剧对标') { bar.classList.remove('show'); return; }
0337:       bar.classList.add('show');
0338:       var h = '';
0339:       for (var i = 0; i < BENCH_STEPS.length; i++) {
0340:         var s = BENCH_STEPS[i], cls = 'pending';
0341:         if (s.id < S.benchStep) cls = 'done';
0342:         else if (s.id === S.benchStep) cls = 'active';
0343: 
0344:         h += '<div class="step-item ' + cls + '" onclick="goBenchStep(' + s.id + ')" title="点击查看此步骤说明">';
0345:         h += '<span class="step-num">' + (cls === 'done' ? '✓' : s.id) + '</span>';
0346:         h += '<span>' + s.icon + ' ' + s.label + '</span>';
0347:         h += '<span class="step-tip">' + getStepTip(s.id) + '</span>';
0348:         h += '</div>';
0349: 
0350:         if (i < BENCH_STEPS.length - 1) {
0351:           h += '<div class="step-connector' + (s.id < S.benchStep ? ' done' : '') + '"></div>';
0352:         }
0353:       }
0354:       inner.innerHTML = h;
0355:     }
0356: 
0357:     function getStepTip(id) {
0358:       var tips = {
0359:         1: '上传参考剧本（.docx或粘贴文本）',
0360:         2: 'AI逐集拆解情节节拍与钩子',
0361:         3: '提取可复用的结构模板',
0362:         4: '确认仿写方案与改编方案',
0363:         5: '基于模板生成仿写大纲',
0364:         6: '审核并确认分集大纲',
0365:         7: '设定剧本输出格式',
0366:         8: '开始逐集生成完整剧本'
0367:       };
0368:       return tips[id] || '';
0369:     }
0370: 
0371:     function goBenchStep(n) {
0372:       if (n < S.benchStep) {
0373:         var p = STEP_PROMPTS[n];
0374:         if (p) { E('chatInput').value = p; E('chatInput').focus(); }
0375:         return;
0376:       }
0377:       if (n === S.benchStep) {
0378:         triggerCurrentStep();
0379:         return;
0380:       }
0381:       alert('请先完成步骤 ' + S.benchStep + '（' + BENCH_STEPS[S.benchStep - 1].label + '）');
0382:     }
0383: 
0384:     function triggerCurrentStep() {
0385:       var step = S.benchStep;
0386:       if (step === 1) {
0387:         E('fileInput').click();
0388:       } else if (step === 4 && tryParseS4()) {
0389:         rP();
0390:       } else if (step === 7 && S.s4) {
0391:         rP();
0392:       } else if (step === 8 && S.s7) {
0393:         nB();
0394:       } else {
0395:         var p = STEP_PROMPTS[step];
0396:         if (p) { E('chatInput').value = p; E('chatInput').focus(); }
0397:       }
0398:     }
0399: 
0400:     function advanceBenchStep(n) {
0401:       if (n > S.benchStep) {
0402:         S.benchStep = n;
0403:         var c = CC(); c.benchStep = n;
0404:         sv(); renderBenchSteps(); rP();
0405:       }
0406:     }
0407: 
0408:     // ====== 面板提取与动态捕获逻辑 =====
0409:     function extractTJ(txt) {
0410:       if (!txt) return null;
0411:       var m = txt.match(/\[TEMPLATEJSON\]\s*([\s\S]*?)\s*\[\/TEMPLATEJSON\]/);
0412:       if (m) { try { return JSON.parse(m[1].trim()); } catch (e) { } }
0413:       var m2 = txt.match(/```json\s*([\s\S]*?)\s*```/);
0414:       if (m2) { try { return JSON.parse(m2[1].trim()); } catch (e) { } }
0415:       var m3 = txt.match(/\{[\s\S]*?"(?:step4_questions|create_questions|questions)"[\s\S]*?\}/);
0416:       if (m3) { try { return JSON.parse(m3[0].trim()); } catch (e) { } }
0417:       return null;
0418:     }
0419: 
0420:     function stripThinking(txt) {
0421:       if (!txt) return '';
0422:       return txt.replace(/<thinking>[\s\S]*?<\/thinking>/gi, '').trim();
0423:     }
0424: 
0425:     function detectOptions(txt) {
0426:       if (!txt) return null;
0427:       var cleanTxt = stripThinking(txt);
0428:       if (!cleanTxt) return null;
0429:       var blocks = [];
0430:       var lines = cleanTxt.split('\n');
0431:       var curQ = null;
0432:       for (var i = 0; i < lines.length; i++) {
0433:         var line = lines[i].trim();
0434:         if (!line) continue;
0435: 
0436:         if (/^(?:已保存|output_|```|===|---|📁|✨|🤖)/i.test(line)) {
0437:           continue;
0438:         }
0439: 
0440:         var optMatch = line.match(/^(?:[A-D][\.\)\s]|(?:\d+\))\s*|选项\s*[A-Z1-9][:：\s]?)\s*(.+)/i);
0441:         if (optMatch && curQ) {
0442:           var optText = optMatch[1].replace(/\*\*/g, '').trim();
0443:           if (optText && optText.length >= 2 && optText.length < 200) {
0444:             curQ.options.push(optText);
0445:             continue;
0446:           }
0447:         }
0448: 
0449:         var isNumHeader = /^(?:\d+[\.、\s]|\*\*\d+[\.、\s]?|【?(?:问题|方向|确认点)\d+】?|Q\d+[:：\s]?)/i.test(line);
0450:         var isQuestionEnd = line.endsWith('？') || line.endsWith('?') || line.endsWith('？）') || line.endsWith('?)');
0451:         var hasQuestionVerb = /你觉得|是否|偏早还是偏晚|如何|哪种|要不要|请确认|倾向|单选|多选|请选择|审核/i.test(line);
0452:         var isForbiddenTitle = /^(?:公式|模板|拆解表格|商业模型|代码块|json|templatejson|已确认|已保存|幻想画面|总结|纲要)/i.test(line);
0453: 
0454:         var isRealQuestion = (isQuestionEnd || hasQuestionVerb) && (isNumHeader || line.length <= 150);
0455: 
0456:         if (isRealQuestion && line.length >= 5 && line.length <= 200 && !isForbiddenTitle) {
0457:           if (curQ) {
0458:             if (!curQ.options || !curQ.options.length) {
0459:               curQ.options = ["A. 认可并按此方案执行", "B. 需要微调（在下方框内说明）", "其他 (请在下方输入框补充说明)"];
0460:             }
0461:             blocks.push(curQ);
0462:           }
0463:           curQ = { question: line.replace(/\*\*/g, '').trim(), options: [] };
0464:         }
0465:       }
0466:       if (curQ) {
0467:         if (!curQ.options || !curQ.options.length) {
0468:           curQ.options = ["A. 认可并按此方案执行", "B. 需要微调（在下方框内说明）", "其他 (请在下方输入框补充说明)"];
0469:         }
0470:         blocks.push(curQ);
0471:       }
0472:       return blocks.length ? blocks : null;
0473:     }
0474: 
0475:     function tryParseS4() {
0476:       var curC = CC();
0477:       var msgs = curC.msgs;
0478:       if (!msgs || !msgs.length) return null;
0479: 
0480:       // 每次只解析最后一条 AI 助手的消息！
0481:       var lastM = null;
0482:       for (var i = msgs.length - 1; i >= 0; i--) {
0483:         if (msgs[i].role === 'assistant' && !msgs[i].er) {
0484:           lastM = msgs[i];
0485:           break;
0486:         }
0487:       }
0488: 
0489:       if (!lastM || !lastM.content) return null;
0490:       // 如果该条消息已点击处理过，避免显示旧卡片
0491:       if (lastM.handled) return null;
0492: 
0493:       // 🔴 剥离 AI 内部思考标签 <thinking>...</thinking>，防止将思考过程解析为面板卡片
0494:       var txt = stripThinking(lastM.content);
0495:       if (!txt) return null;
0496: 
0497:       var d = extractTJ(txt);
0498:       if (d && (d.step4_questions || d.questions || d.step === 'step4_ready' || d.step === 'create_qa_ready')) {
0499:         var qs = d.step4_questions || d.questions;
0500:         if (qs && qs.length) {
0501:           return { step: 'create_qa_ready', questions: qs, step4_questions: qs, msgId: lastM.id };
0502:         }
0503:       }
0504: 
0505:       return null;
0506:     }
0507: 
0508:     function selectOpt(el, qi, optVal) {
0509:       var parent = el.closest('.q-block');
0510:       if (parent) {
0511:         var opts = parent.querySelectorAll('.q-opt');
0512:         for (var i = 0; i < opts.length; i++) opts[i].classList.remove('selected');
0513:       }
0514:       el.classList.add('selected');
0515:       var rad = el.querySelector('input[type=radio]');
0516:       if (rad) rad.checked = true;
0517: 
0518:       var customBox = E('q_custom_' + qi);
0519:       if (customBox) {
0520:         var isOther = /其他|自定义|其它|other|修改|混搭|说明|微调|补充/i.test(optVal);
0521:         customBox.style.display = isOther ? 'block' : 'none';
0522:         if (!isOther) customBox.value = '';
0523:       }
0524:     }
0525: 
0526:     function dismissCards() {
0527:       S.cardsVisible = false;
0528:       var curC = CC(); curC.cardsVisible = false;
0529:       sv();
0530:       E('createPanel').style.display = 'none';
0531:     }
0532: 
0533:     function rP() {
0534:       var cp = E('createPanel'), s4 = E('step4Panel'), s7 = E('step7Panel'), bp = E('batchPanel');
0535: 
0536:       // 🔴 剧本创作模式交互面板：只要 AI 输出 TEMPLATEJSON 或导引问题，动态展示选择面板
0537:       if (S.mode === '剧本创作') {
0538:         var chat = CC();
0539:         var msgs = chat.msgs || [];
0540:         var lastM = msgs.length ? msgs[msgs.length - 1] : null;
0541: 
0542:         if (S.gen || (lastM && lastM.role === 'user')) {
0543:           cp.style.display = 'none';
0544:           return;
0545:         }
0546: 
0547:         var data = tryParseS4();
0548:         if (data && (data.step === 'create_qa_ready' || data.step4_questions || data.questions)) {
0549:           var qs = data.step4_questions || data.questions;
0550:           if (qs && qs.length) {
0551:             cp.style.display = 'block';
0552:             var h = '<div class="panel scroll-panel" style="max-height:300px;overflow-y:auto;"><div style="font-weight:600;font-size:14px;color:var(--primary);margin-bottom:8px;position:sticky;top:0;background:var(--card);padding:4px 0;z-index:5;">🎨 💬 剧本创作 · 需求与方向确认 (请勾选创作倾向)</div>';
0553:             for (var qi = 0; qi < qs.length; qi++) {
0554:               var q = qs[qi];
0555:               h += '<div class="q-block" style="margin-bottom:12px;"><div style="font-weight:600;font-size:13px;margin:6px 0;color:var(--text);">' + esc(q.question) + '</div>';
0556:               if (q.options && q.options.length) {
0557:                 for (var oi = 0; oi < q.options.length; oi++) {
0558:                   var opt = q.options[oi], sel = (oi === 0);
0559:                   h += '<div class="q-opt ' + (sel ? 'selected' : '') + '" onclick="selectOpt(this, ' + qi + ', \'' + esc(opt).replace(/'/g, "\\'") + '\')"><input type="radio" name="cq_' + qi + '" value="' + esc(opt) + '" ' + (sel ? 'checked' : '') + '> <span>' + esc(opt) + '</span></div>';
0560:                 }
0561:               }
0562:               h += '<input type="text" class="input-box q-custom" id="q_custom_' + qi + '" placeholder="请输入你的自定义要求..." style="display:none;margin-top:6px;"></div>';
0563:             }
0564:             h += '<button class="btn primary full" onclick="confirmCreateQA()" style="margin-top:10px;position:sticky;bottom:0;z-index:5;">确认选项，提交AI处理</button></div>';
0565:             cp.innerHTML = h;
0566:             return;
0567:           }
0568:         }
0569: 
0570:         cp.style.display = 'none';
0571:         cp.innerHTML = '';
0572:         return;
0573:       } else {
0574:         cp.style.display = 'none';
0575:       }
0576: 
0577:       // 2. 短剧对标 Step 4 面板 (完全不受影响)
0578:       if (S.mode === '短剧对标' && !S.s4) {
0579:         var data = tryParseS4();
0580:         if (data && (data.step === 'step4_ready' || data.step4_questions || data.questions)) {
0581:           s4.style.display = 'block';
0582:           var h = '<div class="panel scroll-panel" style="max-height:300px;overflow-y:auto;"><div style="font-weight:600;font-size:14px;color:var(--primary);margin-bottom:8px;position:sticky;top:0;background:var(--card);padding:4px 0;z-index:5;">⚡ 💬 基于本剧深度思考提取的核心确认选项 (点击选项高亮)</div>';
0583:           var qs = data.step4_questions || data.questions;
0584:           if (qs && qs.length) {
0585:             for (var qi = 0; qi < qs.length; qi++) {
0586:               var q = qs[qi];
0587:               h += '<div class="q-block" style="margin-bottom:12px;"><div style="font-weight:600;font-size:13px;margin:6px 0;color:var(--text);">' + esc(q.question) + '</div>';
0588:               if (q.options && q.options.length) {
0589:                 for (var oi = 0; oi < q.options.length; oi++) {
0590:                   var opt = q.options[oi], sel = (oi === 0);
0591:                   h += '<div class="q-opt ' + (sel ? 'selected' : '') + '" onclick="selectOpt(this, ' + qi + ', \'' + esc(opt).replace(/'/g, "\\'") + '\')"><input type="radio" name="q_' + qi + '" value="' + esc(opt) + '" ' + (sel ? 'checked' : '') + '> <span>' + esc(opt) + '</span></div>';
0592:                 }
0593:               }
0594:               h += '<input type="text" class="input-box q-custom" id="q_custom_' + qi + '" placeholder="请输入你的自定义仿写要求..." style="display:none;margin-top:6px;"></div>';
0595:             }
0596:           } else {
0597:             h += '<p style="font-size:12px;opacity:.7;margin-bottom:6px;">AI已提出问题，请在下方描述你的仿写方案：</p>';
0598:           }
0599:           h += '<div style="margin-top:8px;"><label style="font-size:12px;opacity:.8;">补充与新设定：</label><textarea id="step4Input" rows="2" placeholder="例：贴身仿写，保留核心公式..."></textarea></div><button class="btn primary full" onclick="cS4()" style="margin-top:10px;position:sticky;bottom:0;z-index:5;">确认方案，生成Step5&6</button></div>';
0600:           s4.innerHTML = h; return;
0601:         }
0602:       }
0603:       s4.style.display = 'none';
0604: 
0605:       // 3. Step 7 面板
0606:       if (S.mode === '短剧对标' && S.s4 && !S.s7) {
0607:         var la = CC().msgs.slice().reverse().find(function (m) { return m.role === 'assistant' && !m.er; });
0608:         if (la && la.content.indexOf('"step":"step7_format"') !== -1) {
0609:           s7.style.display = 'block';
0610:           s7.innerHTML = '<div class="panel"><h4>📐 剧本格式确认</h4><details style="margin-bottom:6px;"><summary style="cursor:pointer;font-size:12px;">默认格式参考</summary><pre style="font-size:11px;background:var(--bg2);padding:8px;border-radius:6px;">集数：第X集   场次：X-Y   场景：简洁\n▲画面描述：简短动作表情\n角色A：台词\n【本集钩子】</pre></details><textarea id="step7Input" rows="3" placeholder="留空=使用默认格式"></textarea><button class="btn primary" onclick="cS7()" style="margin-top:6px;">确认，生成剧本</button></div>';
0611:           return;
0612:         }
0613:       }
0614:       s7.style.display = 'none';
0615: 
0616:       // 4. 批量生成面板
0617:       if (S.mode === '短剧对标' && S.s7 && S.bi > 0) {
0618:         bp.style.display = 'block';
0619:         bp.innerHTML = '<div class="panel"><h4>📦 第' + S.bi + '轮完成（共' + S.tb + '轮）</h4>' + (S.bi < S.tb ? '<button class="btn primary" onclick="nB()" style="margin-top:6px;">继续第' + (S.bi + 1) + '轮</button>' : '') + '</div>';
0620:         return;
0621:       }
0622:       bp.style.display = 'none';
0623:     }
0624: 
0625:     function confirmCreateQA() {
0626:       var sel = [];
0627:       var data = tryParseS4();
0628:       if (data) {
0629:         var qs = data.step4_questions || data.questions;
0630:         if (qs && qs.length) {
0631:           for (var qi = 0; qi < qs.length; qi++) {
0632:             var rad = document.querySelector('input[name="cq_' + qi + '"]:checked');
0633:             if (rad) {
0634:               var val = rad.value;
0635:               var customBox = E('q_custom_' + qi);
0636:               if (customBox && customBox.style.display !== 'none' && customBox.value.trim()) {
0637:                 val = '自定义：' + customBox.value.trim();
0638:               }
0639:               sel.push('Q' + (qi + 1) + '确认: 「' + qs[qi].question + '」 ➔ 意向选择: 「' + val + '」');
0640:             }
0641:           }
0642:         }
0643:       }
0644: 
0645:       var chat = CC();
0646:       if (chat.msgs && chat.msgs.length) {
0647:         for (var i = chat.msgs.length - 1; i >= 0; i--) {
0648:           if (chat.msgs[i].role === 'assistant') {
0649:             chat.msgs[i].handled = true;
0650:             break;
0651:           }
0652:         }
0653:       }
0654: 
0655:       S.step4Questions = null;
0656:       chat.step4Questions = null;
0657:       sv();
0658: 
0659:       var cp = E('createPanel');
0660:       if (cp) { cp.style.display = 'none'; cp.innerHTML = ''; }
0661: 
0662:       var msgText = '## 确认选项\n' + (sel.join('\n') || '按最优创作方案执行');
0663:       E('chatInput').value = msgText;
0664:       sendMsg();
0665:     }
0666: 
0667:     function pickCreateCard(st) {
0668:       S.createStage = st;
0669:       S.cardsVisible = false;
0670:       sv();
0671:       E('chatInput').value = '请继续执行剧本创作【' + st + '】。';
0672:       sendMsg();
0673:     }
0674: 
0675:     function cS4() {
0676:       var sel = [];
0677:       var data = tryParseS4();
0678:       if (data) {
0679:         var qs = data.step4_questions || data.questions;
0680:         if (qs && qs.length) {
0681:           for (var qi = 0; qi < qs.length; qi++) {
0682:             var rad = document.querySelector('input[name="q_' + qi + '"]:checked');
0683:             if (rad) {
0684:               var val = rad.value;
0685:               var customBox = E('q_custom_' + qi);
0686:               if (customBox && customBox.style.display !== 'none' && customBox.value.trim()) {
0687:                 val = '自定义：' + customBox.value.trim();
0688:               }
0689:               sel.push(qs[qi].question + ' => ' + val);
0690:             }
0691:           }
0692:         }
0693:       }
0694:       var v = E('step4Input').value.trim();
0695:       if (v) sel.push('补充设定：' + v);
0696:       S.s4 = true; sv();
0697:       E('step4Panel').style.display = 'none';
0698:       advanceBenchStep(5);
0699:       E('chatInput').value = sel.length ? '以下是我选择的仿写方案：\n' + sel.join('\n') + '\n\n请基于此执行Step5和Step6。' : '贴身仿写，保留原剧核心公式。请执行Step5和Step6。';
0700:       sendMsg();
0701:     }
0702: 
0703:     function cS7() {
0704:       var v = E('step7Input').value.trim();
0705:       S.s7 = true; sv();
0706:       E('step7Panel').style.display = 'none';
0707:       advanceBenchStep(8);
0708:       E('chatInput').value = '确认格式：' + (v || '使用默认格式') + '。请执行Step8，生成第1轮(第1-5集)。';
0709:       sendMsg();
0710:     }
0711: 
0712:     function nB() {
0713:       var ns = S.bi * 5 + 1, ne = Math.min(ns + 4, S.tb * 5);
0714:       E('chatInput').value = '执行Step8第' + (S.bi + 1) + '轮(第' + ns + '-' + ne + '集)，先做回顾。';
0715:       S.bi += 1; sv();
0716:       E('batchPanel').style.display = 'none';
0717:       sendMsg();
0718:     }
0719: 
0720:     // ====== 模式切换 ======
0721:     function toggleMode(m) {
0722:       svs();
0723:       if (S.mode === m) {
0724:         S.mode = null; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.benchStep = 1;
0725:       } else {
0726:         S.mode = m; S.s4 = false; S.s7 = false; S.cstr = false; S.qaHandled = false; S.cardsVisible = true; S.bi = 0; S.benchStep = 1;
0727:       }
0728:       sv(); rf();
0729:     }
0730: 
0731:     // ====== 渲染 ======
0732:     function rf() {
0733:       var s = E('themeSelect');
0734:       s.innerHTML = Object.keys(TH).map(function (t) { return '<option>' + t + '</option>'; }).join('');
0735:       s.value = localStorage.getItem('theme') || '🍑 蜜桃乌龙';
0736:       switchTheme(s.value);
0737: 
0738:       var bB = E('btnBench'), bC = E('btnCreate');
0739:       bB.textContent = '对标' + (S.mode === '短剧对标' ? ' ✓' : '');
0740:       bC.textContent = '创作' + (S.mode === '剧本创作' ? ' ✓' : '');
0741:       bB.className = 'btn' + (S.mode === '短剧对标' ? ' primary' : '');
0742:       bC.className = 'btn' + (S.mode === '剧本创作' ? ' primary' : '');
0743: 
0744:       var ms = JSON.parse(localStorage.getItem('fm') || '["deepseek-chat","deepseek-reasoner","gpt-4o","gpt-4o-mini"]');
0745:       E('modelSelect').innerHTML = ms.map(function (m) { return '<option value="' + m + '">' + m + '</option>'; }).join('');
0746: 
0747:       E('topBar').innerHTML = '';
0748:       rd();
0749:       renderBenchSteps();
0750:       listFiles();
0751:       lds();
0752:       renderHistory();
0753:       E('chatInput').placeholder = '在【' + (S.mode || '通用') + '】模式下输入指令...';
0754:     }
0755: 
0756:     function renderMarkdown(text) {
0757:       if (!text) return '';
0758:       var s = esc(text);
0759: 
0760:       s = s.replace(/\r\n/g, '\n');
0761:       s = s.replace(/\n{3,}/g, '\n\n');
0762: 
0763:       s = s.replace(/```([\s\S]*?)```/g, function(match, code) {
0764:         return '<pre style="background:#f8fafc;padding:10px 12px;border-radius:8px;border:1px solid #e2e8f0;font-family:monospace;font-size:12px;overflow-x:auto;margin:6px 0;white-space:pre-wrap;"><code>' + code + '</code></pre>';
0765:       });
0766: 
0767:       s = s.replace(/^#### (.*$)/gim, '<h5 style="font-size:13px;font-weight:700;margin:8px 0 4px 0;color:#1e293b;">$1</h5>');
0768:       s = s.replace(/^### (.*$)/gim, '<h4 style="font-size:14px;font-weight:700;margin:10px 0 4px 0;color:#2563eb;">$1</h4>');
0769:       s = s.replace(/^## (.*$)/gim, '<h3 style="font-size:15px;font-weight:700;margin:12px 0 4px 0;color:#1e293b;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">$1</h3>');
0770:       s = s.replace(/^# (.*$)/gim, '<h2 style="font-size:16px;font-weight:700;margin:14px 0 6px 0;color:#2563eb;">$1</h2>');
0771: 
0772:       s = s.replace(/^---$/gim, '<hr style="border:none;border-top:1px solid #e2e8f0;margin:8px 0;">');
0773: 
0774:       s = s.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#0f172a;font-weight:700;background:rgba(59,130,246,0.1);padding:1px 4px;border-radius:4px;margin:0 2px;">$1</strong>');
0775: 
0776:       s = s.replace(/\*(.*?)\*/g, '<em style="color:#475569;">$1</em>');
0777: 
0778:       s = s.replace(/^\s*[\-\*]\s+(.*$)/gim, '<div style="margin-left:12px;position:relative;padding-left:12px;margin:2px 0;"><span style="position:absolute;left:0;color:#3b82f6;">•</span>$1</div>');
0779: 
0780:       s = s.replace(/\n/g, '<br>');
0781: 
0782:       s = s.replace(/(?:<br>\s*){3,}/gi, '<br><br>');
0783:       s = s.replace(/(<\/h[2-5]>|<hr>|<\/pre>)\s*<br>/gi, '$1');
0784:       s = s.replace(/<br>\s*(<h[2-5]>|<hr>|<pre)/gi, '$1');
0785: 
0786:       return s.trim();
0787:     }
0788: 
0789:     function rd() {
0790:       var chat = CC(), area = E('chatArea'), h = '', msgs = chat.msgs;
0791:       if (!msgs || !msgs.length) {
0792:         h += '<div style="margin-bottom:12px;background:#dcfce7;border:1px solid #86efac;color:#166534;padding:8px 14px;border-radius:10px;font-size:12px;font-weight:600;display:flex;align-items:center;justify-content:space-between;"><span>✨ 当前已处于全新空白对话 (ID: ' + esc(S.cid) + ')</span><button class="btn xs" onclick="newChat()">清空重置</button></div>';
0793:         if (S.mode === '短剧对标') {
0794:           h += renderBenchGuide();
0795:         } else if (S.mode === '剧本创作') {
0796:           h += '<div class="guide-msg"><div class="guide-title">🎨 剧本创作模式 · 智能分析与追问体验</div><p>请在下方聊天框直接输入你的创作想法或概述（如："我想写一部女扮男装的宫廷追女爽剧..."），发送后 AI 将深入分析并向你提出定向选项卡片供你确认方案。</p></div>';
0797:         } else {
0798:           h += '<div style="text-align:center;padding:60px 0;opacity:.4;font-size:14px;">👆 点击底部「对标」或「创作」开始或在输入框中自由对话 ✨</div>';
0799:         }
0800:         
0801:       if (S.multiSelectMode) {
0802:         var selCount = Object.keys(S.selectedMsgs).filter(function(k){return S.selectedMsgs[k];}).length;
0803:         h += '<div class="batch-bar"><span style="font-size:12px;font-weight:600">已选 ' + selCount + ' 条</span><button class="btn sm danger" onclick="deleteSelectedMsgs()">删除</button><button class="btn sm" onclick="toggleMultiSelect()">取消</button></div>';
0804:       }
0805:       area.innerHTML = h;
0806:         return;
0807:       }
0808: 
0809:       // 🔴 方案 1 性能优化：消息超过 15 条时，开启 UI 视口切片渲染（不影响文件资产存盘与后端全量保存）
0810:       var batchBtn = '';
0811:       if (!S.multiSelectMode && msgs.length > 0) {
0812:         batchBtn = '<div style="text-align:right; margin-bottom:10px;"><button class="btn xs" onclick="toggleMultiSelect()">批量管理</button></div>';
0813:       }
0814:       h += batchBtn;
0815:       var maxVisible = S.showAllMsgs ? msgs.length : 15;
0816:       var startIdx = Math.max(0, msgs.length - maxVisible);
0817: 
0818:       if (startIdx > 0) {
0819:         var hiddenCount = startIdx;
0820:         h += '<div style="text-align:center;margin:6px 0 12px 0;"><button class="btn xs" onclick="S.showAllMsgs=true;rd();" style="background:var(--bg2);border:1px solid var(--border);color:var(--primary);font-weight:600;padding:6px 14px;border-radius:20px;">📜 已折叠更早的 ' + hiddenCount + ' 条历史消息 (点击加载全部对话)</button></div>';
0821:       } else if (S.showAllMsgs && msgs.length > 15) {
0822:         h += '<div style="text-align:center;margin:6px 0 12px 0;"><button class="btn xs" onclick="S.showAllMsgs=false;rd();" style="opacity:.6;padding:4px 10px;border-radius:14px;">收起更早消息</button></div>';
0823:       }
0824: 
0825:       for (var i = startIdx; i < msgs.length; i++) {
0826:         var m = msgs[i];
0827:         if (!S.selectedMsgs) S.selectedMsgs = {};
0828:         h += '<div class="msg-wrap ' + (m.role === 'user' ? 'is-user ' : '') + (S.multiSelectMode ? 'multi-select' : '') + '">';
0829:         if (S.multiSelectMode) {
0830:           h += '<input type="checkbox" class="msg-checkbox" ' + (S.selectedMsgs[i] ? 'checked' : '') + ' onclick="toggleSelectMsg(' + i + ')">';
0831:         }
0832:         if (m.role === 'user') {
0833:           if (S.edi === i) {
0834:             h += '<div class="msg user"><div class="role">👤 你（编辑中）</div><textarea class="edit-textarea" id="editArea" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);">' + esc(m.content) + '</textarea><div class="actions" style="margin-top:4px;"><button class="btn sm primary" onclick="cfEd(' + i + ')">确认</button><button class="btn sm" onclick="S.edi=null;rd()">取消</button></div></div>';
0835:           } else {
0836:             h += '<div class="msg user"><div class="role" style="display:flex;justify-content:space-between"><span>👤 你</span><button class="btn xs" onclick="S.edi=' + i + ';rd()" style="opacity:.4">✏️</button></div><div class="content">' + renderMarkdown(m.content) + '</div></div>';
0837:           }
0838:           h += '</div>'; // close msg-wrap
0839:           continue;
0840:         }
0841:         if (m.er) {
0842:           h += '<div class="err-box"><div style="font-weight:600;margin-bottom:4px;">生成失败</div><div>' + esc(m.content) + '</div>';
0843:           if (i === msgs.length - 1 && !S.gen) h += '<div style="margin-top:6px;"><button class="btn sm" onclick="rgn(' + i + ')">重新生成</button></div>';
0844:           h += '</div>';
0845:           h += '</div>'; // close msg-wrap
0846:           continue;
0847:         }
0848: 
0849:         var rawContent = m.content || '';
0850:         var disp = rawContent;
0851:         if (S.mode === '剧本创作') {
0852:           disp = disp.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, '');
0853:         } else {
0854:           disp = disp.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, '<span style="font-size:11px;opacity:.6;background:var(--bg);padding:1px 6px;border-radius:4px;display:inline-block;margin:2px 0;">📋 (模板数据已解析)</span>');
0855:         }
0856: 
0857:         var thR = /<(?:think|thinking|thought)>([\s\S]*?)(?:<\/(?:think|thinking|thought)>|$)/gi, thH = '', tm;
0858:         while ((tm = thR.exec(disp)) !== null) {
0859:           if (tm[1]) thH += tm[1] + '\n';
0860:         }
0861:         disp = disp.replace(/<(?:think|thinking|thought)>[\s\S]*?(?:<\/(?:think|thinking|thought)>|$)/gi, '').trim();
0862: 
0863:         var isGenerating = m.s || (S.gen && i === msgs.length - 1);
0864: 
0865:         h += '<div class="msg assistant"><div class="role">🤖 助手</div>';
0866:         if (thH.trim()) h += '<details class="think-box"><summary>🧠 思考过程 (点击展开/折叠)</summary><div style="margin-top:6px;opacity:.95;">' + renderMarkdown(thH.trim()) + '</div></details>';
0867:         if (isGenerating) h += '<div class="think-box">🤔 AI 正在思考中<div class="dots"><span></span><span></span><span></span></div></div>';
0868:         h += '<div class="content" id="msg_' + (m.id || '') + '">' + renderMarkdown(disp) + '</div>';
0869: 
0870:         if (i === msgs.length - 1 && !m.s && !S.gen) {
0871:           h += '<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap;">';
0872:           h += '<button class="btn sm" onclick="rgn(' + i + ')">重新生成</button>';
0873:           if (S.mode === '短剧对标' && S.benchStep <= 8) {
0874:             var nextPrompt = STEP_PROMPTS[S.benchStep];
0875:             if (nextPrompt) {
0876:               h += '<button class="btn sm primary" onclick="E(\'chatInput\').value=\'' + esc(nextPrompt).replace(/'/g, "\\'") + '\';E(\'chatInput\').focus();">继续步骤' + S.benchStep + ' →</button>';
0877:             }
0878:           }
0879:           h += '</div>';
0880:         }
0881:         h += '</div>'; // close msg assistant
0882:         h += '</div>'; // close msg-wrap
0883:       }
0884:       
0885:       if (S.multiSelectMode) {
0886:         var selCount = Object.keys(S.selectedMsgs).filter(function(k){return S.selectedMsgs[k];}).length;
0887:         h += '<div class="batch-bar"><span style="font-size:12px;font-weight:600">已选 ' + selCount + ' 条</span><button class="btn sm danger" onclick="deleteSelectedMsgs()">删除</button><button class="btn sm" onclick="toggleMultiSelect()">取消</button></div>';
0888:       }
0889:       area.innerHTML = h;
0890:       area.scrollTop = area.scrollHeight;
0891:       rP();
0892:     }
0893: 
0894:     function renderBenchGuide() {
0895:       var h = '<div class="guide-msg">';
0896:       h += '<div class="guide-title">🔬 短剧对标模式 · 8步流程</div>';
0897:       h += '<p style="margin-bottom:8px;">此模式将引导你完成：上传参考剧本 → 拆解分析 → 提取模板 → 仿写方案 → 生成仿写剧本。</p>';
0898:       h += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;font-size:12px;">';
0899:       for (var i = 0; i < BENCH_STEPS.length; i++) {
0900:         var s = BENCH_STEPS[i], isCurrent = (s.id === S.benchStep);
0901:         h += '<div style="padding:4px 0;' + (isCurrent ? 'color:var(--primary);font-weight:700;' : 'opacity:.7;') + '">' + (isCurrent ? '👉 ' : '') + s.icon + ' Step' + s.id + ': ' + s.label + '</div>';
0902:       }
0903:       h += '</div>';
0904:       h += '<div style="margin-top:10px;padding-top:8px;border-top:1px solid #e5e7eb;">';
0905:       h += '<span style="font-weight:600;">📍 当前：Step ' + S.benchStep + ' - ' + BENCH_STEPS[S.benchStep - 1].label + '</span> ';
0906:       h += '<span style="font-size:12px;opacity:.7;">— ' + getStepTip(S.benchStep) + '</span>';
0907:       h += '<div class="preset-btns">';
0908:       if (S.benchStep === 1) {
0909:         h += '<span class="preset-btn" onclick="E(\'fileInput\').click()">📁 上传参考剧本</span>';
0910:         h += '<span class="preset-btn" onclick="E(\'chatInput\').value=\'请帮我对标分析我上传的参考剧本，先确认已收到并阅读完毕。\';E(\'chatInput\').focus();">📤 已上传，开始分析</span>';
0911:       } else {
0912:         var p = STEP_PROMPTS[S.benchStep];
0913:         if (p) h += '<span class="preset-btn" onclick="E(\'chatInput\').value=\'' + esc(p).replace(/'/g, "\\'") + '\';E(\'chatInput\').focus();">🚀 执行 Step ' + S.benchStep + '</span>';
0914:       }
0915:       h += '</div></div></div>';
0916:       return h;
0917:     }
0918: 
0919:     function rgn(idx) {
0920:       var c = CC();
0921:       c.msgs = c.msgs.slice(0, idx);
0922:       sv(); rd();
0923:       sendMsg(true);
0924:     }
0925: 
0926:     // ====== 发送消息与 done 强制检测逻辑 ======
0927:     async function sendMsg(isRegen) {
0928:       if (typeof isRegen !== 'boolean') isRegen = false;
0929:       var inp = E('chatInput'), txt = inp.value.trim();
0930:       
0931:       var chat = CC();
0932:       var lastM = chat.msgs && chat.msgs.length ? chat.msgs[chat.msgs.length - 1] : null;
0933:       if (S.gen && (!lastM || !lastM.s)) {
0934:         S.gen = false;
0935:       }
0936: 
0937:       if ((!txt && !isRegen) || S.gen) return;
0938: 
0939:       if (S.mode === '剧本创作') {
0940:         S.cardsVisible = false;
0941:         chat.cardsVisible = false;
0942:       }
0943: 
0944:       if (!isRegen) inp.value = '';
0945:       var k = gK(); if (!k) { alert('请先填写API Key'); return; }
0946: 
0947:       if (!isRegen && txt) {
0948:         if (!chat.msgs.length || chat.msgs[chat.msgs.length - 1].content !== txt) chat.msgs.push({ role: 'user', content: txt });
0949:       }
0950:       sv(); rd();
0951: 
0952:       var docT = '';
0953:       if (S.doc && (S.mode === '短剧对标' || S.mode === '剧本创作') && chat.msgs.filter(function (m) { return m.role === 'user'; }).length <= 2) {
0954:         docT = S.doc;
0955:       }
0956: 
0957:       if (S.mode === '短剧对标') {
0958:         if (S.benchStep === 1 && txt.indexOf('已上传') !== -1) advanceBenchStep(2);
0959:         else if (S.benchStep === 2 && (txt.indexOf('拆解') !== -1 || txt.indexOf('拉片') !== -1)) advanceBenchStep(3);
0960:       }
0961: 
0962:       S.gen = true; S.ab = new AbortController();
0963:       E('topBar').innerHTML = '<button class="btn danger" onclick="stopGen()">⏹ 停止生成</button>';
0964:       E('chatInput').disabled = true;
0965: 
0966:       var pid = 'm' + Date.now();
0967:       chat.msgs.push({ role: 'assistant', content: '', s: true, id: pid });
0968:       rd();
0969: 
0970:       try {
0971:         var r = await fetch(B + '/api/chat', {
0972:           method: 'POST',
0973:           headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()),
0974:           body: JSON.stringify({
0975:             api_key: k, api_url: gU(), model: gM(), work_mode: S.mode || '通用',
0976:             messages: chat.msgs.filter(function (m) { return !m.s; }).map(function (m) { return { role: m.role, content: m.content }; }),
0977:             user_input: txt, doc_text: docT, session_id: S.cid, token: getToken()
0978:           }),
0979:           signal: S.ab.signal
0980:         });
0981: 
0982:         var reader = r.body.getReader(), dec = new TextDecoder(), buf = '', full = '';
0983:         while (true) {
0984:           var rdv = await reader.read(); if (rdv.done) break;
0985:           buf += dec.decode(rdv.value, { stream: true });
0986:           var lines = buf.split('\n'); buf = lines.pop() || '';
0987:           for (var li = 0; li < lines.length; li++) {
0988:             var l = lines[li]; if (!l.startsWith('data: ')) continue;
0989:             try {
0990:               var d = JSON.parse(l.slice(6));
0991:               if (d.token) {
0992:                 full += d.token;
0993:                 var m = chat.msgs.find(function (x) { return x.id === pid; });
0994:                 if (m) m.content = full;
0995:                 var el = E("msg_" + pid);
0996:                 if (el) {
0997:                   el.innerHTML = renderMarkdown(full.replace(/\[TEMPLATEJSON\][\s\S]*?\[\/TEMPLATEJSON\]/g, ""));
0998:                   let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 150;
0999:                   if(isAtB2) E("chatArea").scrollTop = E("chatArea").scrollHeight;
1000:                   rP();
1001:                 } else {
1002:                   rd();
1003:                 }
1004:               } else if (d.type === 'done') {
1005:                 var m = chat.msgs.find(function (x) { return x.id === pid; });
1006:                 if (m) { delete m.s; delete m.id; m.content = full; if (d.saved_file) m.content += '\n\n---\n📁 已保存: ' + d.saved_file; }
1007: 
1008:                 var sdir = d.session_dir || d.sessiondir;
1009:                 if (sdir) S.sd = sdir;
1010: 
1011:                 if (S.mode === '短剧对标' && S.benchStep === 3) {
1012:                   advanceBenchStep(4);
1013:                   S.s4 = false;
1014:                 }
1015: 
1016:                 S.step4Questions = null;
1017:                 if (d.template_json) {
1018:                   S.step4Questions = d.template_json;
1019:                   var curC = CC();
1020:                   curC.step4Questions = d.template_json;
1021:                   var s = d.template_json.step;
1022:                   if (s === 'step4_ready') S.s4 = false;
1023:                   else if (s === 'step7_format') S.s7 = false;
1024:                   else if (s === 'batch_complete') { S.bi = d.template_json.batch_index || 1; S.tb = d.template_json.total_batches || 0; }
1025:                 }
1026: 
1027:                 var dyn = tryParseS4();
1028:                 if (dyn && (dyn.step === 'step4_ready' || dyn.step4_questions || dyn.questions)) {
1029:                   if (S.mode === '短剧对标') {
1030:                     S.s4 = false;
1031:                     advanceBenchStep(4);
1032:                   }
1033:                 }
1034: 
1035:                 sv(); rd(); listFiles();
1036:               } else if (d.type === 'error') {
1037:                 var m = chat.msgs.find(function (x) { return x.id === pid; });
1038:                 if (m) { m.content = d.message; m.er = true; delete m.s; delete m.id; }
1039:                 rd();
1040:               }
1041:             } catch (e) { }
1042:           }
1043:         }
1044:       } catch (e) {
1045:         var m = chat.msgs.find(function (x) { return x.id === pid; });
1046:         if (e.name !== 'AbortError') {
1047:           if (m) { m.content = '请求失败：' + e.message; m.er = true; delete m.s; delete m.id; }
1048:         } else {
1049:           if (m) { m.content += '\n\n[用户停止了生成]'; delete m.s; delete m.id; }
1050:         }
1051:       }
1052: 
1053:       S.gen = false; S.ab = null;
1054:       E('topBar').innerHTML = ''; E('chatInput').disabled = false; E('chatInput').focus();
1055:       rd(); sv();
1056:     }
1057: 
1058:     function stopGen() { if (S.ab) S.ab.abort(); }
1059:     function cfEd(idx) {
1060:       var c = CC(), nv = E('editArea').value.trim();
1061:       if (nv) { c.msgs[idx].content = nv; c.msgs = c.msgs.slice(0, idx + 1); }
1062:       S.edi = null; sv(); rd();
1063:     }
1064: 
1065:     // ====== 文件操作与删除 ======
1066:     function clearDoc() {
1067:       S.doc = '';
1068:       var inp = E('fileInput'); if (inp) inp.value = '';
1069:       E('fileInfo').innerHTML = '未选择文件';
1070:       showToast('🗑️ 参考脚本已成功清除！');
1071:     }
1072: 
1073:     async function handleFileUpload(inp) {
1074:       var files = inp.files;
1075:       if (!files || !files.length) return;
1076:       S.doc = '';
1077:       var texts = [], infos = [];
1078:       E('fileInfo').innerHTML = '⏳ 正在解析 ' + files.length + ' 个文件...';
1079:       for (var i = 0; i < files.length; i++) {
1080:         var f = files[i];
1081:         var fd = new FormData();
1082:         fd.append('file', f);
1083:         try {
1084:           var r = await fetch(B + '/api/upload', { method: 'POST', body: fd });
1085:           var d = await r.json();
1086:           if (d.text) {
1087:             texts.push('【文件' + (i + 1) + ': ' + d.filename + '】\n' + d.text);
1088:             infos.push(d.filename + '（' + d.word_count + '字）');
1089:           }
1090:         } catch (e) { }
1091:       }
1092:       if (texts.length) {
1093:         S.doc = texts.join('\n\n---\n\n');
1094:         E('fileInfo').innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px;"><span>✅ 已成功合并上传 ' + texts.length + ' 个文件</span><button class="btn xs danger" onclick="clearDoc()">🗑️ 清除</button></div><div style="font-size:11px;opacity:.7;margin-top:2px;">' + infos.join('<br>') + '</div>';
1095:         if (S.mode === '短剧对标') advanceBenchStep(2);
1096:       } else {
1097:         E('fileInfo').innerHTML = '<span style="color:#ff6b6b">上传失败</span>';
1098:       }
1099:     }
1100: 
1101:     async function listFiles() {
1102:       if (!S.sd) S.sd = 'session_' + S.cid;
1103:       var sid = S.sd.replace(/\\/g, '/').split('/').pop();
1104:       try {
1105:         var r = await fetch(B + '/api/files/' + sid + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() }), d = await r.json();
1106:         if (d.files && d.files.length) {
1107:           E('projectFiles').innerHTML = d.files.map(function (f) {
1108:             return '<div style="margin:4px 0;display:flex;justify-content:space-between;align-items:center;background:var(--bg);padding:4px 8px;border-radius:6px;border:1px solid var(--border);">' +
1109:               '<span style="cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:140px;" onclick="pv(\'' + f.path + '\')" title="' + esc(f.name) + '">📄 ' + esc(f.name) + '</span>' +
1110:               '<div style="display:flex;gap:4px;">' +
1111:               '<a href="' + B + '/api/download/' + f.path + '" download class="btn xs" style="text-decoration:none" title="下载">⬇</a>' +
1112:               '<button class="btn xs danger" onclick="delFile(\'' + f.path + '\')" title="物理删除文件">🗑️</button>' +
1113:               '</div></div>';
1114:           }).join('');
1115:         } else E('projectFiles').innerHTML = '暂无';
1116:       } catch (e) { E('projectFiles').innerHTML = '暂无'; }
1117:     }
1118: 
1119:     async function delFile(path) {
1120:       if (!confirm('确定要物理删除该文件吗？')) return;
1121:       try {
1122:         var r = await fetch(B + '/api/delete/' + path + '?token=' + encodeURIComponent(getToken()), { method: 'DELETE', headers: getAuthHeaders() });
1123:         var d = await r.json();
1124:         if (d.status === 'ok') {
1125:           showToast('🗑️ 文件已成功删除！');
1126:           E('previewBox').style.display = 'none';
1127:           listFiles();
1128:         } else {
1129:           alert('删除失败：' + (d.error || '未知错误'));
1130:         }
1131:       } catch (e) {
1132:         alert('删除请求失败：' + e.message);
1133:       }
1134:     }
1135: 
1136:     async function pv(path) {
1137:       try {
1138:         E('editorPane').style.display = 'flex';
1139:         E('editorFileName').innerText = '加载中...';
1140:         E('editorContent').innerText = '正在读取文件内容，请稍候...';
1141:         E('editorSaveStatus').innerText = '';
1142:         currentPreviewFile = path;
1143: 
1144:         var t = '';
1145:         try {
1146:           var r = await fetch(B + '/api/preview/' + path + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() });
1147:           if (r.ok) {
1148:             var d = await r.json();
1149:             t = d.text || d.error || '';
1150:           } else {
1151:             var r2 = await fetch(B + '/api/download/' + path);
1152:             t = await r2.text();
1153:           }
1154:         } catch(netErr) {
1155:           t = '网络请求失败，请检查服务器是否正常运行。' + netErr.message;
1156:         }
1157:         
1158:         // 只有当用户没有切换到其他文件时才更新
1159:         if (currentPreviewFile === path) {
1160:           E('editorFileName').innerText = path.split('/').pop();
1161:           E('editorContent').innerText = t;
1162:           updateWordCount();
1163:         }
1164:       } catch (e) { 
1165:         if (currentPreviewFile === path) {
1166:           E('editorContent').innerText = '读取失败: ' + e.message;
1167:         }
1168:       }
1169:     }
1170: 
1171:     async function fetchModels() {
1172:       var k = gK(), u = gU();
1173:       if (!k) { alert('请先填写API Key'); return; }
1174:       try {
1175:         var r = await fetch(B + '/api/fetch-models', { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()), body: JSON.stringify({ api_key: k, api_url: u }) });
1176:         var d = await r.json();
1177:         if (d.models && d.models.length) {
1178:           E('modelSelect').innerHTML = d.models.map(function (m) { return '<option value="' + m + '">' + m + '</option>'; }).join('');
1179:           localStorage.setItem('fm', JSON.stringify(d.models));
1180:           svs();
1181:           E('apiStatus').className = 'status-tag ok'; E('apiStatus').innerHTML = '🟢 已连接(' + d.models.length + ')';
1182:           alert('拉取成功：' + d.models.length + '个模型');
1183:         } else alert('拉取失败：' + (d.error || '无模型返回'));
1184:       } catch (e) { alert('拉取失败：' + e.message); }
1185:     }
1186: 
1187:     
1188:     // ====== 用户鉴权与历史同步逻辑 ======
1189:     var currentAuthTab = 'login';
1190: 
1191:     function getToken() {
1192:       return localStorage.getItem('auth_token') || '';
1193:     }
1194: 
1195:     function getAuthHeaders() {
1196:       var t = getToken();
1197:       return t ? { 'Authorization': 'Bearer ' + t } : {};
1198:     }
1199: 
1200:     function openAuthModal() {
1201:       document.getElementById('authModal').style.display = 'flex';
1202:       document.getElementById('authErrMsg').style.display = 'none';
1203:     }
1204: 
1205:     function closeAuthModal() {
1206:       document.getElementById('authModal').style.display = 'none';
1207:     }
1208: 
1209:     function switchAuthTab(tab) {
1210:       currentAuthTab = tab;
1211:       document.getElementById('authErrMsg').style.display = 'none';
1212:       if (tab === 'login') {
1213:         document.getElementById('authTabLogin').classList.add('active');
1214:         document.getElementById('authTabRegister').classList.remove('active');
1215:         document.getElementById('authSubmitBtn').innerText = '🔑 立即登录';
1216:       } else {
1217:         document.getElementById('authTabRegister').classList.add('active');
1218:         document.getElementById('authTabLogin').classList.remove('active');
1219:         document.getElementById('authSubmitBtn').innerText = '✨ 注册新账号';
1220:       }
1221:     }
1222: 
1223:     async function checkAuthStatus() {
1224:       var token = getToken();
1225:       if (!token) {
1226:         // openAuthModal();
1227:         updateUserBadge(null);
1228:         return;
1229:       }
1230:       try {
1231:         var r = await fetch(B + '/api/auth/me?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
1232:         var d = await r.json();
1233:         if (d.user && d.user.username) {
1234:           updateUserBadge(d.user.username);
1235:           closeAuthModal();
1236:           loadUserHistorySessions();
1237:         } else {
1238:           openAuthModal();
1239:           updateUserBadge(null);
1240:         }
1241:       } catch (e) {
1242:         updateUserBadge(null);
1243:       }
1244:     }
1245: 
1246:     function updateUserBadge(username) {
1247:       if (username) {
1248:         document.getElementById('userNameShow').innerHTML = '👤 ' + esc(username);
1249:         document.getElementById('userAuthActionBtn').innerText = '🚪 退出';
1250:         document.getElementById('userAuthActionBtn').onclick = logoutUser;
1251:       } else {
1252:         document.getElementById('userNameShow').innerHTML = '👤 未登录';
1253:         document.getElementById('userAuthActionBtn').innerText = '🔑 登录';
1254:         document.getElementById('userAuthActionBtn').onclick = openAuthModal;
1255:       }
1256:     }
1257: 
1258:     async function submitAuth() {
1259:       var u = document.getElementById('authUsername').value.trim();
1260:       var p = document.getElementById('authPassword').value.trim();
1261:       var errBox = document.getElementById('authErrMsg');
1262:       errBox.style.display = 'none';
1263: 
1264:       if (!u || !p) {
1265:         errBox.innerText = '用户名和密码不能为空！';
1266:         errBox.style.display = 'block';
1267:         return;
1268:       }
1269: 
1270:       var endpoint = currentAuthTab === 'login' ? '/api/auth/login' : '/api/auth/register';
1271:       try {
1272:         var r = await fetch(B + endpoint, {
1273:           method: 'POST',
1274:           headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders()),
1275:           body: JSON.stringify({ username: u, password: p })
1276:         });
1277:         var d = await r.json();
1278:         if (d.status === 'ok') {
1279:           localStorage.setItem('auth_token', d.token);
1280:           localStorage.setItem('auth_username', d.username);
1281:           showToast(currentAuthTab === 'login' ? '🎉 登录成功！' : '🎉 注册成功并已登录！');
1282:           closeAuthModal();
1283:           checkAuthStatus();
1284:         } else {
1285:           errBox.innerText = d.message || '操作失败，请重试';
1286:           errBox.style.display = 'block';
1287:         }
1288:       } catch (e) {
1289:         errBox.innerText = '连接服务器失败：' + e.message;
1290:         errBox.style.display = 'block';
1291:       }
1292:     }
1293: 
1294:     function logoutUser() {
1295:       if (confirm('确定要退出登录吗？')) {
1296:         localStorage.removeItem('auth_token');
1297:         localStorage.removeItem('auth_username');
1298:         updateUserBadge(null);
1299:         openAuthModal();
1300:       }
1301:     }
1302: 
1303:     async function loadUserHistorySessions() {
1304:       var token = getToken();
1305:       if (!token) return;
1306:       try {
1307:         var r = await fetch(B + '/api/history/list?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
1308:         var d = await r.json();
1309:         if (d.sessions && d.sessions.length) {
1310:           
1311:           // 将所有远程的 session 注入到 S.chats 里，这样 renderHistorySelect 才能渲染它们
1312:           d.sessions.forEach(function(s) {
1313:             var exists = S.chats.find(function(c) { return c.id === s.session_id; });
1314:             if (!exists) {
1315:               S.chats.push({ id: s.session_id, title: s.title, msgs: [], sd: null, mode: s.mode, benchStep: 1, step4Questions: null, cstr: false, qaHandled: false, cardsVisible: true });
1316:             }
1317:           });
1318:           
1319:           var sel = document.getElementById('historySelect');
1320:           if (sel) {
1321:             // ...
1322:             sel.innerHTML = S.chats.map(function(c) {
1323:               return '<option value="' + c.id + '">' + esc(c.title || '对话') + '</option>';
1324:             }).join('');
1325:             
1326:             sel.value = S.cid;
1327:             if (sel.value !== S.cid) {
1328:                sel.value = d.sessions[0].session_id;
1329:             }
1330:             try {
1331:               var cidToFetch = sel.value || S.cid;
1332:               var r2 = await fetch(B + '/api/history/detail/' + cidToFetch + '?token=' + encodeURIComponent(token), { headers: getAuthHeaders() });
1333:               var d2 = await r2.json();
1334:               if (d2.status === 'ok' && d2.messages) {
1335:                 S.cid = cidToFetch;
1336:                 var targetC = CC();
1337:                 targetC.msgs = d2.messages;
1338:                 sv(); rf();
1339:               }
1340:             } catch(e) {}
1341:           }
1342:         }
1343:       } catch(e) {}
1344:     }
1345: 
1346:     function exportHistory() {
1347:       if (!S.chats || S.chats.length === 0) {
1348:         alert("没有可导出的历史记录");
1349:         return;
1350:       }
1351:       var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(S.chats, null, 2));
1352:       var downloadAnchorNode = document.createElement('a');
1353:       downloadAnchorNode.setAttribute("href", dataStr);
1354:       downloadAnchorNode.setAttribute("download", "history_backup.json");
1355:       document.body.appendChild(downloadAnchorNode);
1356:       downloadAnchorNode.click();
1357:       downloadAnchorNode.remove();
1358:     }
1359: 
1360:     async function importHistory(event) {
1361:       var file = event.target.files[0];
1362:       if (!file) return;
1363:       var reader = new FileReader();
1364:       reader.onload = async function(e) {
1365:         try {
1366:           var importedChats = JSON.parse(e.target.result);
1367:           if (!Array.isArray(importedChats)) {
1368:             alert("导入的文件格式不正确！");
1369:             return;
1370:           }
1371:           if (!S.chats) S.chats = [];
1372:           
1373:           var newCount = 0;
1374:           importedChats.forEach(function(ic) {
1375:             var exists = S.chats.find(function(c) { return c.id === ic.id; });
1376:             if (!exists) {
1377:               S.chats.push(ic);
1378:               newCount++;
1379:             }
1380:           });
1381:           
1382:           sv();
1383:           rf();
1384:           
1385:           if (newCount > 0) {
1386:             alert("成功导入了 " + newCount + " 条新记录。正在自动同步到云端...");
1387:             var token = getToken();
1388:             if (token) {
1389:               try {
1390:                 var res = await fetch(B + '/api/history/sync', {
1391:                   method: 'POST',
1392:                   headers: Object.assign({'Content-Type': 'application/json'}, getAuthHeaders()),
1393:                   body: JSON.stringify({
1394:                     token: token,
1395:                     chats: importedChats
1396:                   })
1397:                 });
1398:                 var d = await res.json();
1399:                 if (d.status === 'ok') {
1400:                   alert("云端同步完成！成功同步了 " + d.synced_count + " 条记录。");
1401:                   loadUserHistorySessions(); // 刷新云端列表
1402:                 } else {
1403:                   alert("云端同步失败: " + d.message);
1404:                 }
1405:               } catch(err) {
1406:                 alert("云端同步请求出错，请确保你已登录并且网络畅通。");
1407:               }
1408:             } else {
1409:               alert("导入成功，但你未登录账号，无法同步到云端。");
1410:             }
1411:           } else {
1412:             alert("没有发现新的记录，所有记录已存在。");
1413:           }
1414:         } catch(err) {
1415:           alert("解析备份文件失败: " + err.message);
1416:         }
1417:         document.getElementById('importFile').value = "";
1418:       };
1419:       reader.readAsText(file);
1420:     }
1421: 
1422:     ld(); lds(); rf(); checkAuthStatus();
1423:   
1424:     // Quote feature
1425:     document.addEventListener('mouseup', function(e) {
1426:       if(e.target.id === 'quoteBtn') return;
1427:       setTimeout(() => {
1428:         let sel = window.getSelection();
1429:         let text = sel.toString().trim();
1430:         let btn = document.getElementById('quoteBtn');
1431:         if (!text) {
1432:             btn.style.display = 'none';
1433:             return;
1434:         }
1435:         let rect = sel.getRangeAt(0).getBoundingClientRect();
1436:         btn.style.display = 'block';
1437:         btn.style.left = Math.max(10, rect.left + (rect.width / 2) - 35) + 'px';
1438:         btn.style.top = Math.max(10, rect.top - 40) + 'px';
1439:       }, 10);
1440:     });
1441:     document.addEventListener('mousedown', function(e) {
1442:       if(e.target.id !== 'quoteBtn') {
1443:           let btn = document.getElementById('quoteBtn');
1444:           if(btn) btn.style.display = 'none';
1445:       }
1446:     });
1447:     function handleQuote() {
1448:       let sel = window.getSelection();
1449:       let text = sel.toString().trim();
1450:       if(text) {
1451:           let input = document.getElementById('chatInput');
1452:           let existing = input.value;
1453:           input.value = '> ' + text + '\n\n' + existing;
1454:           input.focus();
1455:           document.getElementById('quoteBtn').style.display = 'none';
1456:           window.getSelection().removeAllRanges();
1457:           
1458:           window.pendingQuoteContext = {
1459:               text: text,
1460:               file: window.currentPreviewFile || null
1461:           };
1462:       }
1463:     }
1464:     
1465:   
1466:     async function applySmartPatch(msgId, ctxStr) {
1467:         var ctx = JSON.parse(decodeURIComponent(ctxStr));
1468:         var c = S.chats.find(function(x) { return x.id === S.cid; });
1469:         var m = c.msgs.find(function(x) { return x.id === msgId; });
1470:         if (!m) return;
1471:         
1472:         var newText = m.content.trim();
1473:         var oldText = ctx.text;
1474:         var file = ctx.file;
1475:         
1476:         if (window.currentPreviewFile !== file) {
1477:             await pv(file);
1478:             // wait for render
1479:             await new Promise(r => setTimeout(r, 500));
1480:         }
1481:         
1482:         var editor = document.getElementById('editorContent');
1483:         var currentContent = editor.innerText;
1484:         
1485:         if (currentContent.indexOf(oldText) === -1) {
1486:             // Try stripping leading/trailing whitespace which might have been altered
1487:             var strippedOld = oldText.replace(/^\s+|\s+$/g, '');
1488:             if (currentContent.indexOf(strippedOld) !== -1) {
1489:                 oldText = strippedOld;
1490:             } else {
1491:                 alert("在文档中找不到原始引用的文本，可能已经被手动修改过了。");
1492:                 return;
1493:             }
1494:         }
1495:         
1496:         var updatedContent = currentContent.replace(oldText, newText);
1497:         editor.innerText = updatedContent;
1498:         
1499:         await saveEditorContent();
1500:         
1501:         removeSmartPatch(msgId);
1502:         
1503:         // Show success animation or alert
1504:         var btn = document.getElementById('btnCreate');
1505:         var oldBtnText = btn ? btn.innerText : '';
1506:         if(btn) {
1507:             btn.innerText = '✅ 覆写成功！';
1508:             setTimeout(() => btn.innerText = oldBtnText, 2000);
1509:         } else {
1510:             alert("✅ 覆写成功并已保存！");
1511:         }
1512:     }
1513: 
1514:     function removeSmartPatch(msgId) {
1515:         var c = S.chats.find(function(x) { return x.id === S.cid; });
1516:         var m = c.msgs.find(function(x) { return x.id === msgId; });
1517:         if (m) {
1518:             delete m.quoteContext;
1519:             sv();
1520:             rf();
1521:         }
1522:     }
1523: 
1524: 