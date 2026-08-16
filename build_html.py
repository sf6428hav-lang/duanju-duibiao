"""运行这个脚本，自动生成 创作工坊.html"""
import os

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>创作工坊</title>
<style>
:root{--bg:#fef9f4;--bg2:#fdf0e5;--text:#5c4a3d;--primary:#e8937a;--card:#ffffff;--border:#f5d5c6;--shadow:0 4px 20px rgba(232,147,122,0.12);--radius:12px;--err-bg:#fff0f0;--err-border:#ffcccc;--dot:#e8937a}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);height:100vh;overflow:hidden}
.app{display:flex;height:100vh}
@keyframes td{0%,60%,100%{opacity:0.2;transform:translateY(0)}30%{opacity:1;transform:translateY(-6px)}}
@keyframes slideUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.sidebar{width:310px;min-width:310px;background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto;padding:14px;gap:10px;z-index:10}
.sidebar h4{font-size:12px;font-weight:600;color:var(--primary);margin:6px 0 2px}
.sidebar label{font-size:11px;opacity:.7}
.sidebar select,.sidebar input[type=text],.sidebar input[type=password]{width:100%;padding:7px 9px;border-radius:7px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:12px;margin:2px 0}
.btn{padding:7px 12px;border-radius:var(--radius);border:1px solid var(--border);background:var(--card);color:var(--text);font-size:12px;cursor:pointer;transition:all .2s;font-weight:500;white-space:nowrap}
.btn:hover{border-color:var(--primary);color:var(--primary);transform:translateY(-1px)}
.btn.primary{background:var(--primary);color:#fff;border-color:var(--primary)}
.btn.full{width:100%}
.btn.sm{padding:4px 8px;font-size:11px}
.btn.danger{background:#ff6b6b;color:#fff;border-color:#ff6b6b}
.row{display:flex;gap:6px}
.row>*{flex:1}
.main{flex:1;display:flex;flex-direction:column;overflow:hidden}
.header{text-align:center;padding:16px 0 8px;flex-shrink:0}
.header h3{font-size:18px;font-weight:600}
.header p{font-size:12px;opacity:.6;margin-top:2px}
.top-bar{padding:0 20px;flex-shrink:0}
.chat-area{flex:1;overflow-y:auto;padding:8px 20px;display:flex;flex-direction:column;gap:10px}
.chat-area:empty::after{content:"输入需求，开始创作吧 \\2728";display:block;text-align:center;color:var(--text);opacity:.3;padding:60px 0;font-size:14px}
.panel{background:var(--card);border:2px solid var(--primary);border-radius:14px;padding:16px;margin:8px 0;box-shadow:var(--shadow)}
.panel h4{color:var(--primary);font-size:14px;margin-bottom:6px}
.panel textarea{width:100%;border-radius:7px;border:1px solid var(--border);padding:9px;font-size:13px;background:var(--bg);color:var(--text);resize:vertical}
.msg{background:var(--card);border-radius:14px;border:1px solid var(--border);box-shadow:var(--shadow);padding:12px 14px;animation:slideUp .3s ease}
.msg .role{font-size:11px;font-weight:600;margin-bottom:4px;opacity:.5}
.msg .content{line-height:1.7;font-size:14px;white-space:pre-wrap;word-break:break-word}
.msg .actions{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap}
.think-box{background:var(--bg2);border:1px dashed var(--border);border-radius:10px;padding:9px 12px;margin-bottom:8px;font-size:12px;opacity:.85}
.think-box summary{color:var(--primary);font-weight:600;cursor:pointer;font-size:12px}
.err-box{background:var(--err-bg);border:1px solid var(--err-border);border-radius:10px;padding:10px 14px;margin:4px 0}
.err-box .err-title{color:#ff6b6b;font-weight:600;font-size:13px;margin-bottom:4px}
.err-box .err-body{font-size:13px;opacity:.8}
.bottom-bar{padding:10px 20px 14px;flex-shrink:0;display:flex;gap:8px;align-items:center}
.bottom-bar input[type=text]{flex:1;padding:9px 14px;border-radius:22px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:14px;outline:none}
.bottom-bar input[type=text]:focus{border-color:var(--primary)}
.preview{background:var(--bg2);border-radius:10px;padding:12px;max-height:200px;overflow-y:auto;margin:8px 0;font-size:12px;white-space:pre-wrap}
.dots{display:inline-flex;gap:4px;margin-left:6px}
.dots span{width:5px;height:5px;border-radius:50%;background:var(--dot);animation:td 1.4s infinite}
.dots span:nth-child(2){animation-delay:.2s}
.dots span:nth-child(3){animation-delay:.4s}
.collapse-header{cursor:pointer;user-select:none;font-weight:600;font-size:12px;padding:5px 0;display:flex;align-items:center;gap:5px}
.collapse-header::before{content:'\\25B8';display:inline-block;transition:transform .2s;font-size:9px}
.collapse-header.open::before{transform:rotate(90deg)}
.collapse-body{display:none}
.collapse-body.open{display:block}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.edit-textarea{width:100%;min-height:60px;border-radius:7px;border:1px solid var(--primary);padding:8px;font-size:14px;background:var(--card);color:var(--text);resize:vertical}
.hist-item{display:flex;align-items:center;justify-content:space-between;padding:3px 0}
.hist-item .del-btn{font-size:10px;padding:2px 5px;opacity:.4;cursor:pointer;border:none;background:none;color:var(--text)}
.hist-item .del-btn:hover{opacity:1;color:#ff6b6b}
</style>
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar">
<h4>🎨 主题切换</h4>
<select id="themeSelect" onchange="switchTheme(this.value)"></select>
<hr style="border-color:var(--border);opacity:.5">
<h4>💬 历史对话</h4>
<button class="btn primary full" onclick="newChat()">+ 新建对话</button>
<div id="historyList" style="max-height:200px;overflow-y:auto;font-size:12px;"></div>
<hr style="border-color:var(--border);opacity:.5">
<div class="collapse-header open" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open')">⚙️ API 设置</div>
<div class="collapse-body open">
<label>API Key</label>
<input type="password" id="apiKey" placeholder="sk-..." onchange="saveSet()">
<label>API URL</label>
<input type="text" id="apiUrl" value="https://yunwu.ai/v1" onchange="saveSet()">
<label>模型</label>
<select id="modelSelect" onchange="saveSet()"></select>
<input type="text" id="customModel" placeholder="或手动输入模型ID" onchange="saveSet()" style="margin-top:3px;">
<button class="btn full sm" onclick="fetchModels()" style="margin-top:4px;">🔄 拉取可用模型</button>
</div>
<hr style="border-color:var(--border);opacity:.5">
<h4>📂 参考脚本上传</h4>
<input type="file" id="fileUpload" accept=".docx" onchange="handleFileUpload(this)" style="font-size:11px;">
<div id="fileInfo" style="font-size:11px;opacity:.7;"></div>
<hr style="border-color:var(--border);opacity:.5">
<h4>📁 生成文件</h4>
<div id="projectFiles" style="font-size:11px;opacity:.7;">暂无</div>
</aside>
<main class="main">
<div class="header"><h3>Hello，今天想创作些什么？</h3><p>输入你的需求，开始创作吧！</p></div>
<div class="top-bar" id="topBar"></div>
<div id="previewBox" style="display:none;padding:0 20px;"></div>
<div id="step4Panel" style="display:none;padding:0 20px;"></div>
<div class="chat-area" id="chatArea"></div>
<div id="step7Panel" style="display:none;padding:0 20px;"></div>
<div id="batchPanel" style="display:none;padding:0 20px;"></div>
<div class="bottom-bar">
<button class="btn" id="btnBench" onclick="toggleMode('短剧对标')">对标</button>
<button class="btn" id="btnCreate" onclick="toggleMode('剧本创作')">创作</button>
<input type="text" id="chatInput" placeholder="输入指令..." onkeydown="if(event.key==='Enter')sendMsg()">
<button class="btn primary" onclick="sendMsg()">发送</button>
</div>
</main>
</div>

<script>
var B='http://localhost:8000';
var TH={
"🍑 蜜桃乌龙":{bg:"#fef9f4",bg2:"#fdf0e5",text:"#5c4a3d",primary:"#e8937a",card:"#ffffff",border:"#f5d5c6",shadow:"0 4px 20px rgba(232,147,122,0.12)",radius:"12px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#e8937a"},
"🫧 气泡苏打":{bg:"#f6fafe",bg2:"#eaf4fd",text:"#3d5064",primary:"#7eb8da",card:"#ffffff",border:"#d0e7f5",shadow:"0 4px 20px rgba(126,184,218,0.10)",radius:"16px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#7eb8da"},
"🍋 柠檬跳跳糖":{bg:"#fffef5",bg2:"#fff9db",text:"#5a5530",primary:"#f0c040",card:"#ffffff",border:"#f5e8a0",shadow:"0 4px 20px rgba(240,192,64,0.10)",radius:"10px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#f0c040"},
"🧸 小熊软糖":{bg:"#fbf7f4",bg2:"#f5ede6",text:"#5c4638",primary:"#c4956a",card:"#ffffff",border:"#e8d5c4",shadow:"0 4px 20px rgba(196,149,106,0.10)",radius:"14px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#c4956a"},
"🖋 墨纸禅意":{bg:"#fafaf8",bg2:"#f2f2ee",text:"#2c2c2c",primary:"#3a3a3a",card:"#ffffff",border:"#e0e0dc",shadow:"0 2px 12px rgba(0,0,0,0.04)",radius:"6px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#3a3a3a"},
"🌙 月光灰调":{bg:"#f5f5f7",bg2:"#eaeaef",text:"#2d2d3a",primary:"#5b5b8a",card:"#ffffff",border:"#dcdce5",shadow:"0 2px 16px rgba(91,91,138,0.06)",radius:"8px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#5b5b8a"},
"🪨 暖石灰":{bg:"#f9f6f3",bg2:"#f0ece8",text:"#4a4540",primary:"#8b7e6e",card:"#ffffff",border:"#e2ddd6",shadow:"0 2px 12px rgba(139,126,110,0.06)",radius:"8px",eb:"#fff0f0",ebd:"#ffcccc",dot:"#8b7e6e"},
"🌿 薄荷暗色":{bg:"#1e2328",bg2:"#161a1e",text:"#d0d6d8",primary:"#68b893",card:"#262c32",border:"#353d45",shadow:"0 4px 20px rgba(0,0,0,0.25)",radius:"10px",eb:"#3a1a1a",ebd:"#ff6b6b",dot:"#68b893"},
"🫐 蓝莓暗夜":{bg:"#1a1d2e",bg2:"#141726",text:"#c8cddb",primary:"#7c8ce0",card:"#232740",border:"#353b58",shadow:"0 4px 20px rgba(0,0,0,0.30)",radius:"10px",eb:"#3a1a1a",ebd:"#ff6b6b",dot:"#7c8ce0"},
"🖤 曜石极简":{bg:"#111111",bg2:"#0a0a0a",text:"#cccccc",primary:"#eeeeee",card:"#1a1a1a",border:"#333333",shadow:"0 4px 20px rgba(0,0,0,0.40)",radius:"4px",eb:"#3a1a1a",ebd:"#ff6b6b",dot:"#eeeeee"}
};
var S={cid:'c'+Date.now(),mode:null,chats:[],doc:'',s4:false,s7:false,bi:0,tb:0,gen:false,ab:null,sd:null,edi:null};
function sv(){localStorage.setItem('app',JSON.stringify({cid:S.cid,mode:S.mode,chats:S.chats,s4:S.s4,s7:S.s7,bi:S.bi,tb:S.tb,sd:S.sd}))}
function ld(){try{var d=JSON.parse(localStorage.getItem('app'));if(d){S.cid=d.cid  S.cid;S.mode=d.mode;S.chats=d.chats  [];S.s4=d.s4  false;S.s7=d.s7  false;S.bi=d.bi  0;S.tb=d.tb  0;S.sd=d.sd}}catch(e){}}
function svs(){localStorage.setItem('apis',JSON.stringify({k:E('apiKey').value,u:E('apiUrl').value,m:E('customModel').value  E('modelSelect').value}))}
function lds(){try{var d=JSON.parse(localStorage.getItem('apis'));if(d){E('apiKey').value=d.k  '';E('apiUrl').value=d.u  'https://yunwu.ai/v1';if(d.m)E('customModel').value=d.m}}catch(e){}}
function E(id){return document.getElementById(id)}
function esc(s){return(s  '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function CC(){var c=S.chats.find(function(x){return x.id===S.cid});if(!c){c={id:S.cid,title:'新对话',msgs:[],sd:null};S.chats.unshift(c)}return c}
function newChat(){var c=CC();if(c.msgs.length){var f=c.msgs.find(function(m){return m.role==='user'});c.title=f?f.content.replace(/[#*\\[\\]【】\\s]/g,'').slice(0,14):'对话'}c.mode=S.mode;c.sd=S.sd;S.cid='c'+Date.now();S.mode=null;S.s4=false;S.s7=false;S.bi=0;S.tb=0;S.sd=null;sv();rf()}
function swChat(id){if(id===S.cid)return;var c=CC();if(c.msgs.length){var f=c.msgs.find(function(m){return m.role==='user'});c.title=f?f.content.replace(/[#*\\[\\]【】\\s]/g,'').slice(0,14):'对话'}c.mode=S.mode;c.sd=S.sd;sv();S.cid=id;c=CC();S.mode=c.mode;S.sd=c.sd;S.s4=false;S.s7=false;S.bi=0;sv();rf()}
function delChat(id){S.chats=S.chats.filter(function(c){return c.id!==id});if(S.cid===id)newChat();else{sv();rf()}}
function swT(n){var t=TH[n],r=document.documentElement.style;r.setProperty('--bg',t.bg);r.setProperty('--bg2',t.bg2);r.setProperty('--text',t.text);r.setProperty('--primary',t.primary);r.setProperty('--card',t.card);r.setProperty('--border',t.border);r.setProperty('--shadow',t.shadow);r.setProperty('--radius',t.radius);r.setProperty('--err-bg',t.eb);r.setProperty('--err-border',t.ebd);r.setProperty('--dot',t.dot);localStorage.setItem('theme',n)}
function gM(){return E('customModel').value.trim()  E('modelSelect').value  'gpt-4o'}
function gK(){return E('apiKey').value.trim()}
function gU(){return E('apiUrl').value.trim()  'https://yunwu.ai/v1'}
async function fetchModels(){var k=gK(),u=gU();if(!k){alert('请先填写API Key');return}try{var r=await fetch(B+'/api/fetch-models',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({apikey:k,apiurl:u})});var d=await r.json();if(d.models&&d.models.length){E('modelSelect').innerHTML=d.models.map(function(m){return '<option value="'+m+'">'+m+'</option>'}).join('');localStorage.setItem('fm',JSON.stringify(d.models));alert('拉取成功：'+d.models.length+'个模型')}else alert('拉取失败：'+(d.error  '无模型返回'))}catch(e){alert('拉取失败：'+e.message)}}
async function handleFileUpload(inp){var f=inp.files[0];if(!f)return;var fd=new FormData();fd.append('file',f);try{var r=await fetch(B+'/api/upload',{method:'POST',body:fd});var d=await r.json();S.doc=d.text  '';E('fileInfo').innerHTML=d.error?'<span style="color:#ff6b6b">'+d.error+'</span>':'✅ '+d.filename+'（'+d.word_count+'字）'}catch(e){E('fileInfo').innerHTML='<span style="color:#ff6b6b">上传失败</span>'}}
async function listFiles(){if(!S.sd){E('projectFiles').innerHTML='暂无';return}var sid=S.sd.replace(/\\\\/g,'/').split('/').pop();try{var r=await fetch(B+'/api/files/'+sid),d=await r.json();if(d.files&&d.files.length){E('projectFiles').innerHTML=d.files.map(function(f){return '<div style="margin:3px 0;display:flex;justify-content:space-between;align-items:center;"><span style="cursor:pointer" onclick="pv(\\''+f.path+'\\')">📄 '+f.name+'</span><a href="'+B+'/api/download/'+f.path+'" download class="btn sm" style="text-decoration:none">⬇</a></div>'}).join('')}else E('projectFiles').innerHTML='暂无'}catch(e){E('projectFiles').innerHTML='暂无'}}
async function pv(path){try{var r=await fetch(B+'/api/download/'+path),t=await r.text();E('previewBox').style.display='block';E('previewBox').innerHTML='<div class="panel"><div style="display:flex;justify-content:space-between;align-items:center;"><h4>📖 '+path.split('/').pop()+'</h4><button class="btn sm" onclick="E(\\'previewBox\\').style.display=\\'none\\'">✕</button></div><div class="preview">'+esc(t)+'</div></div>';E('previewBox').scrollIntoView()}catch(e){}}
async function sendMsg(){var inp=E('chatInput'),txt=inp.value.trim();if(!txt  S.gen)return;inp.value='';var k=gK();if(!k){alert('请先填写API Key');return}var chat=CC();if(!chat.msgs.length  chat.msgs[chat.msgs.length-1].content!==txt)chat.msgs.push({role:'user',content:txt});sv();rd();var docT='';if(S.doc&&S.mode==='短剧对标'&&chat.msgs.filter(function(m){return m.role==='user'}).length<=2)docT=S.doc;S.gen=true;S.ab=new AbortController();E('topBar').innerHTML='<button class="btn danger" onclick="stopGen()">⏹ 停止生成</button>';E('chatInput').disabled=true;var pid='m'+Date.now();chat.msgs.push({role:'assistant',content:'',s:true,id:pid});rd();try{var r=await fetch(B+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({apikey:k,apiurl:gU(),model:gM(),workmode:S.mode  '通用',messages:chat.msgs.filter(function(m){return !m.s}).map(function(m){return{role:m.role,content:m.content}}),userinput:txt,doctext:docT}),signal:S.ab.signal});var reader=r.body.getReader(),dec=new TextDecoder(),buf='',full='';while(true){var rdv=await reader.read();if(rdv.done)break;buf+=dec.decode(rdv.value,{stream:true});var lines=buf.split('\\n');buf=lines.pop()  '';for(var li=0;li<lines.length;li++){var l=lines[li];if(!l.startsWith('data: '))continue;try{var d=JSON.parse(l.slice(6));if(d.token){full+=d.token;var m=chat.msgs.find(function(x){return x.id===pid});if(m)m.content=full;rd()}else if(d.type==='done'){var m=chat.msgs.find(function(x){return x.id===pid});if(m){delete m.s;delete m.id;m.content=full;if(d.savedfile)m.content+='\\n\\n---\\n📁 已保存: '+d.savedfile}if(d.sessiondir)S.sd=d.sessiondir;if(d.templatejson){var s=d.templatejson.step;if(s==='step4ready'  s==='step4ready')S.s4=false;else if(s==='step7format')S.s7=false;else if(s==='batchcomplete'){S.bi=d.templatejson.batchindex  1;S.tb=d.templatejson.totalbatches  0}}sv();rd();listFiles()}else if(d.type==='error'){var m=chat.msgs.find(function(x){return x.id===pid});if(m){m.content=d.message;m.er=true;delete m.s;delete m.id}rd()}}catch(e){}}}}catch(e){if(e.name!=='AbortError'){var m=chat.msgs.find(function(x){return x.id===pid});if(m){m.content='请求失败：'+e.message;m.er=true;delete m.s;delete m.id}}else{var m=chat.msgs.find(function(x){return x.id===pid});if(m){m.content+='\\n\\n[用户停止了生成]';delete m.s;delete m.id}}rd()}S.gen=false;S.ab=null;E('topBar').innerHTML='';E('chatInput').disabled=false;E('chatInput').focus();sv()}
function stopGen(){if(S.ab)S.ab.abort()}
function rd(){var chat=CC(),area=E('chatArea'),h='',msgs=chat.msgs;for(var i=0;i<msgs.length;i++){var m=msgs[i];if(m.role==='user'){if(S.edi===i){h+='<div class="msg"><div class="role">👤 你（编辑中）</div><textarea class="edit-textarea" id="editArea">'+esc(m.content)+'</textarea><div class="actions"><button class="btn sm primary" onclick="cfEd('+i+')">确认</button><button class="btn sm" onclick="S.edi=null;rd()">取消</button></div></div>'}else{h+='<div class="msg"><div class="role" style="display:flex;justify-content:space-between"><span>👤 你</span><button class="btn sm" onclick="S.edi='+i+';rd()" style="opacity:.4">✏️</button></div><div class="content">'+esc(m.content)+'</div></div>'}continue}if(m.er){h+='<div class="err-box"><div class="err-title">生成失败</div><div class="err-body">'+esc(m.content)+'</div>';if(i===msgs.length-1&&!S.gen)h+='<div class="actions"><button class="btn sm" onclick="rgn('+i+')">重新生成</button></div>';h+='</div>';continue}var disp=m.content  '';disp=disp.replace(/\\[TEMPLATEJSON\\][\\s\\S]?\\[\\/TEMPLATEJSON\\]/g,'\\n\\n📋 (模板数据已解析)\\n\\n');var thR=/<(?:thinking thought)>([\\s\\S]?)<\\/(?:thinking thought)>/g;var thH='',tm;while((tm=thR.exec(disp))!==null)thH+=tm[1];disp=disp.replace(/<(?:thinking thought)>[\\s\\S]?<\\/(?:thinking thought)>/g,'');var oT=disp.match(/<(?:thinking thought)>(?![\\s\\S]<\\/(?:thinking thought)>)/);var cM='[请说继续获取下一段]',hc=cM&&disp.indexOf(cM)!==-1;if(hc)disp=disp.replace(cM,'');h+='<div class="msg"><div class="role">🤖 助手</div>';if(thH)h+='<details class="think-box"><summary>思考过程</summary>'+esc(thH)+'</details>';if(oT)h+='<div class="think-box">🤔 思考中<div class="dots"><span></span><span></span><span></span></div></div>';h+='<div class="content">'+esc(disp)+'</div>';if(i===msgs.length-1&&!m.s&&!S.gen){h+='<div class="actions"><button class="btn sm" onclick="rgn('+i+')">重新生成</button>';if(hc)h+='<button class="btn sm primary" onclick="ctG()">继续生成</button>';h+='</div>'}h+='</div>'}area.innerHTML=h;area.scrollTop=area.scrollHeight;rP()}
function rgn(idx){var c=CC();c.msgs=c.msgs.slice(0,idx);sv();rd()}
function ctG(){E('chatInput').value='继续';sendMsg()}
function cfEd(idx){var c=CC(),nv=E('editArea').value.trim();if(nv){c.msgs[idx].content=nv;c.msgs=c.msgs.slice(0,idx+1)}S.edi=null;sv();rd()}
function rP(){var chat=CC(),s4=E('step4Panel'),s7=E('step7Panel'),bp=E('batchPanel');if(S.mode==='短剧对标'&&!S.s4){var la=chat.msgs.slice().reverse().find(function(m){return m.role==='assistant'&&!m.er});if(la&&(la.content.indexOf('"step":"step4ready"')!==-1  la.content.indexOf('"step":"step4ready"')!==-1)){s4.style.display='block';s4.innerHTML='<div class="panel"><h4>📝 仿写方案填写</h4><p style="font-size:12px;opacity:.7;margin-bottom:6px;">AI已提出6个问题，在此描述你的仿写方案。</p><textarea id="step4Input" rows="4" placeholder="例：贴身仿写，保留核心公式..."></textarea><button class="btn primary" onclick="cS4()" style="margin-top:6px;">确认方案，生成Step5&6</button></div>';return}}s4.style.display='none';if(S.mode==='短剧对标'&&S.s4&&!S.s7){var la=chat.msgs.slice().reverse().find(function(m){return m.role==='assistant'&&!m.er});if(la&&la.content.indexOf('"step":"step7format"')!==-1){s7.style.display='block';s7.innerHTML='<div class="panel"><h4>📐 剧本格式确认</h4><details style="margin-bottom:6px;"><summary style="cursor:pointer;font-size:12px;">默认格式参考</summary><pre style="font-size:11px;background:var(--bg2);padding:8px;border-radius:6px;">集数：第X集   场次：X-Y   场景：简洁\\n▲画面描述：简短动作表情\\n角色A：台词\\n【本集钩子】</pre></details><textarea id="step7Input" rows="3" placeholder="留空=使用默认格式"></textarea><button class="btn primary" onclick="cS7()" style="margin-top:6px;">确认，生成剧本</button></div>';return}}s7.style.display='none';if(S.mode==='短剧对标'&&S.s7&&S.bi>0){bp.style.display='block';bp.innerHTML='<div class="panel"><h4>📦 第'+S.bi+'轮完成（共'+S.tb+'轮）</h4>'+(S.bi<S.tb?'<button class="btn primary" onclick="nB()" style="margin-top:6px;">继续第'+(S.bi+1)+'轮</button>':'')+'</div>';return}bp.style.display='none'}
function cS4(){var v=E('step4Input').value.trim();S.s4=true;sv();E('step4Panel').style.display='none';E('chatInput').value=v?'以下是我对仿写方案的描述，请基于此执行Step5和Step6：\\n\\n'+v:'贴身仿写，保留原剧核心公式。请执行Step5和Step6。';sendMsg()}
function cS7(){var v=E('step7Input').value.trim();S.s7=true;sv();E('step7Panel').style.display='none';E('chatInput').value='确认格式：'+(v  '使用默认格式')+'。请执行Step8，生成第1轮(第1-5集)。';sendMsg()}
function nB(){var ns=S.bi5+1,ne=Math.min(ns+4,S.tb5);E('chatInput').value='执行Step8第'+(S.bi+1)+'轮(第'+ns+'-'+ne+'集)，先做回顾。';S.bi+=1;sv();E('batchPanel').style.display='none';sendMsg()}
function toggleMode(m){if(S.mode===m){S.mode=null;S.s4=false;S.s7=false;S.bi=0}else{S.mode=m;S.s4=false;S.s7=false;S.bi=0}sv();rf()}
function rf(){var s=E('themeSelect');s.innerHTML=Object.keys(TH).map(function(t){return'<option>'+t+'</option>'}).join('');s.value=localStorage.getItem('theme')  '🍑 蜜桃乌龙';swT(s.value);var bB=E('btnBench'),bC=E('btnCreate');bB.textContent='对标'+(S.mode==='短剧对标'?' ✓':'');bC.textContent='创作'+(S.mode==='剧本创作'?' ✓':'');bB.className='btn'+(S.mode==='短剧对标'?' primary':'');bC.className='btn'+(S.mode==='剧本创作'?' primary':'');var ms=JSON.parse(localStorage.getItem('fm')  '["deepseek-chat","deepseek-reasoner","gpt-4o","gpt-4o-mini"]');E('modelSelect').innerHTML=ms.map(function(m){return'<option value="'+m+'">'+m+'</option>'}).join('');var hl=E('historyList'),hc='';for(var i=0;i<S.chats.length;i++){var c=S.chats[i],t=c.title  '新对话',is=c.id===S.cid;hc+='<div class="hist-item"><span style="cursor:pointer;'+(is?'color:var(--primary);font-weight:600':'')+'" onclick="swChat(\\''+c.id+'\\')">'+(is?'👉 ':'  ')+t+'</span><button class="del-btn" onclick="event.stopPropagation();delChat(\\''+c.id+'\\')">✕</button></div>'}hl.innerHTML=hc  '<span style="opacity:.4">暂无历史</span>';E('topBar').innerHTML='';rd();rP();listFiles();E('chatInput').placeholder='在【'+(S.mode  '通用')+'】模式下输入指令...'}
ld();lds();rf();
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "创作工坊.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"已生成：{out}")
print("双击打开即可使用（需先启动 backend.py）")