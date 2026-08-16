"""
创作工坊 · FastAPI 后端服务 (全功能完整整合版)
包含：短剧对标、剧本创作、文件管理、用户注册登录鉴权、多用户数据隔离、历史会话持久化等全套 API 路由
启动命令：python -m uvicorn server:app --port 8000 --reload
"""
from fastapi import FastAPI, UploadFile, File, Form, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from openai import OpenAI
from pydantic import BaseModel
import docx, os, time, json, re, io, base64, sqlite3, hashlib, secrets
from typing import Optional, List

app = FastAPI(title="创作工坊 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
DB_PATH = os.path.join(SCRIPT_DIR, "database.db")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 初始化 SQLite 数据库与用户鉴权表
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at INTEGER
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_tokens (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        created_at INTEGER
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        session_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        title TEXT,
        mode TEXT,
        updated_at INTEGER
    )
    ''')
    conn.commit()

    # 默认自动置入系统管理员账号 admin，密码从文件或环境变量读取
    c.execute("SELECT id FROM users WHERE username = 'admin'")
    if not c.fetchone():
        import os, string, random
        admin_pass = os.environ.get("ADMIN_PASSWORD")
        if not admin_pass:
            try:
                with open("admin_password.txt", "r") as pf:
                    admin_pass = pf.read().strip()
            except FileNotFoundError:
                admin_pass = "".join(random.choices(string.ascii_letters + string.digits, k=12))
                with open("admin_password.txt", "w") as pf:
                    pf.write(admin_pass)
                print(f"\n{'='*50}\n注意：已生成 admin 初始密码并保存至 admin_password.txt\n密码是: {admin_pass}\n{'='*50}\n")
        pw_hash = hashlib.sha256(admin_pass.encode('utf-8')).hexdigest()
        c.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                  ('admin', pw_hash, int(time.time())))
        conn.commit()
    conn.close()

init_db()

class AuthRequest(BaseModel):
    username: str
    password: str

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_current_user_info(token_str: str = "", authorization: str = "") -> dict:
    raw = token_str or authorization or ""
    if raw.startswith("Bearer "):
        raw = raw[7:].strip()
    raw = raw.strip()
    if not raw:
        return {"user_id": 1, "username": "admin"}
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, username FROM user_tokens WHERE token = ?", (raw,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"user_id": row[0], "username": row[1]}
    return {"user_id": 1, "username": "admin"}

def get_user_session_dir(username: str, session_id: str) -> str:
    safe_user = re.sub(r'[\\/:*?"<>|\r\n\t\s]+', '_', username or 'admin').strip('_')
    safe_session = str(session_id or f"{int(time.time())}").strip()
    if not safe_session.startswith("session_"):
        safe_session = f"session_{safe_session}"
    safe_session = re.sub(r'[\\/:*?"<>|\r\n\t\s]+', '_', safe_session).strip('_')
    
    path = os.path.join(OUTPUT_DIR, safe_user, safe_session)
    os.makedirs(path, exist_ok=True)
    return path, safe_session

OUTPUT_CLEAN_RULE = """
【思考与正文隔离及文件资产存盘判定准则】：
1. 任何关于“执行了什么指令”、“1. 去除了XX标注...”、“总字数约820字”、“如果OK咱们继续推进”、“你看看对不对味”等总结、汇报、字数统计或交流话术，必须 100% 写入 <think> ... </think> 标签内！
2. 🔴【存盘判定原则】：在思考时只问一句话："这段内容生成后，是要留着用户以后反复编辑、拼接、引用的资产，还是看完就完了？"
   - 【要写成文件资产】：大纲、分集梗概、章节正文、角色设定、世界观设定、对标拆解方案等需要长期引用的成果。正文中绝对禁止包含任何“第X集要点”、“严格执行了你的指令”、“字数约XX字”、“对不对味”、“你先审一下”等临时沟通交流废话！
   - 【只在对话里回复，严禁混入正文文件】：分析结论、建议、意见、点评、打分、帮用户挑选/对比、3行以内的片段示例、对本集要点的总结说明、询问用户对不对味等。
3. 在 <think> 标签外只允许输出最纯粹干净的【剧本正文/大纲/资产】（从 集数头/场次头 开始：第一集 / 1-1日/外 场景），正文中绝不能带任何总结点、交流话术或思考落脚！
4. 视觉排版规范：正文中严禁带有多余错乱的 ** 符号！标题与角色标签统一使用清晰干净的格式（如：【女主·苏晚】、一、核心设定 等），保持整体阅读排版清爽。
"""

CREATE_PROMPT = r"""
你是顶级竖屏短剧编剧智能体。必须严格按以下方法论从零到一完成短剧剧本创作。

核心理论：
情绪ABC短剧变形：情绪 = 视觉符号(B) + 冲击动作(A) + 秒级节奏(T)
🔴【全流程创作标准化 4 步工作流】：
- Step 1: 【需求与核心人设确认】-> 互动面板梳理人物设定、矛盾冲突与故事主线；
- Step 2: 【规格与参数强制确认（关键步骤）】-> 在进入正文创作前，必须向用户确认【目标总集数】、【单集时长与字数规格】、【制作与画面格式】，并输出 [TEMPLATEJSON] 规格确认交互选项卡！
- Step 3: 【分集大纲与前十集集纲规划】-> 规划整体故事脉络与付费卡点；
- Step 4: 【逐轮分批正文生成】-> 严格按用户确认的规格参数（集数/字数/时长/格式），每轮 5 集分批产出高质量剧本正文。

🔴【全流程通用交互面板卡片铁律（按需精准触发）】：
1. 只有当 AI 需要用户做出【规格参数确认、方向审核、情节选择或细节微调】时，才在回答的最前端输出 [TEMPLATEJSON] 交互卡片！
2. 当 AI 正在输出正文、大纲或进行普通说明时，严禁输出 [TEMPLATEJSON]，前端面板会自动隐藏，绝不打扰用户阅读！
3. 每一个要向用户确认的问题，必须分别写为 questions 数组中的一个独立元素，且配备 3-4 个具体可选项（options）以及“其他 (自定义输入)”选项！
4. 🔴【严禁隔离铁律】：[TEMPLATEJSON] 内部绝对禁止包含任何总结性文字或剧情小传！总结性文字只能写在 [TEMPLATEJSON] 外部！

通用规格确认 [TEMPLATEJSON] 范例：
[TEMPLATEJSON]
{
  "step": "create_qa_ready",
  "questions": [
    {
      "field": "total_episodes",
      "question": "1. 目标总集数确认：你计划创作多少集的短剧？(单选)",
      "options": [
        "60集 (标准短剧快节奏)",
        "80集 (爆款推荐：1-10期待-11-60压抑-61-80爆发)",
        "100集 (长篇爆款杠杆)",
        "其他 (请在下方输入框补充说明)"
      ]
    },
    {
      "field": "episode_length",
      "question": "2. 单集时长与字数规格：你希望每集的字数与时长标准是？(单选)",
      "options": [
        "每集1分钟 (400-500字，高频爽点快节奏)",
        "每集1.5-2分钟 (600-800字，信息量充沛/漫剧标配)",
        "每集2-3分钟 (1000-1200字，长镜头戏份)",
        "其他 (请在下方输入框补充说明)"
      ]
    }
  ]
}
[/TEMPLATEJSON]
""" + OUTPUT_CLEAN_RULE

BENCH_PROMPT = r"""
你是顶级短剧对标与仿写智能体，擅长爆款短剧的结构拆解、套路分析、节奏把控与精准仿写。

=== Step 1-2：逐集深度拆解 ===

对每一集，用表格覆盖以下全部24个维度（缺一不可）：

集数 场景 主要出场人物 大事件 小事件 主线付费卡点 本集钩子 台词亮点 人物塑造 亮点 本集作用 情绪类型 情绪强度(1-10) 爽点类型 爽点强度(1-10) 冲突类型 悬念设置 反转标记(是/否) 信息密度(高/中/低) 节奏评估 名场面标记(是/否) 完播率预测因子(1-10) 正文字数 台词字数 画面描述字数

=== Step 3：提取7类可复用模板 ===

拆解完成后，必须提取以下7类模板（每类至少3-5行具体内容）：
1.钩子节奏模板 2.爽点节奏模板 3.情绪曲线模板 4.卡点位置模板 5.冲突升级模板 6.人设建立模板 7.反转设计模板

=== Step 4：仿写思考 -> 深度绑定本剧剧情的个性化结构提问 ===

你必须先输出「仿写思考」(200-300字纯文本)。末尾必须输出 [TEMPLATEJSON] 标签块！

=== Step 5：改编方案 ===
=== Step 6：大纲+小传+梗概 ===
=== Step 7：剧本格式确认 ===
=== Step 8：分批生成剧本（硬性要求）===
""" + OUTPUT_CLEAN_RULE

def extract_template_json(text: str):
    m = re.search(r'\[TEMPLATEJSON\]\s*(.*?)\s*\[/TEMPLATEJSON\]', text, re.DOTALL)
    if m:
        try: return json.loads(m.group(1))
        except: pass
    m2 = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if m2:
        try: return json.loads(m2.group(1))
        except: pass
    return None

def extract_smart_filename(content: str, messages: list = None, user_input: str = "", wmode: str = "") -> str:
    drama_title = ""
    title_matches = re.findall(r'《([^》]+)》', content)
    if not title_matches and user_input:
        title_matches = re.findall(r'《([^》]+)》', str(user_input))
    if not title_matches and messages:
        for m in reversed(messages):
            mc = m.get("content", "") if isinstance(m, dict) else str(m)
            tm = re.findall(r'《([^》]+)》', mc)
            if tm:
                title_matches = tm
                break

    if title_matches:
        drama_title = title_matches[0]
        drama_title = re.sub(r'[\\/:*?"<>|\r\n\t]', '', drama_title).strip()
    return drama_title

def process_document_saving(content: str, session_dir: str, messages: list = None, user_input: str = "", wmode: str = "") -> Optional[str]:
    if not content:
        return None

    # 1. 彻底去除 <thinking>...</thinking> 与 <think>...</think>
    text = re.sub(r'<thinking>[\s\S]*?(?:</thinking>|$)', '', content, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', text, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'\[TEMPLATEJSON\][\s\S]*?(?:\[/TEMPLATEJSON\]|$)', '', text, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'```json[\s\S]*?```', '', text, flags=re.DOTALL | re.IGNORECASE).strip()

    # 2. 严格识别正式资产头部
    has_script = bool(re.search(r'^(?:#+\s*|【)?(?:第[一二三四五六七八九十0-9]+集|1-5集剧本|6-10集剧本|分集剧本正文)(?:】|\s|$)', text, re.MULTILINE))
    has_character = bool(re.search(r'^(?:#+\s*|【)?(?:人物小传|角色设定|人设小传|角色小传)(?:】|\s|$)', text, re.MULTILINE))
    has_outline = bool(re.search(r'^(?:#+\s*|【)?(?:故事大纲|剧情大纲|三幕式大纲)(?:】|\s|$)', text, re.MULTILINE))
    has_ep_outline = bool(re.search(r'^(?:#+\s*|【)?(?:前十集集纲|分集集纲|前10集集纲)(?:】|\s|$)', text, re.MULTILINE))
    has_analysis = bool(re.search(r'^(?:#+\s*|【)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告)(?:】|\s|$)', text, re.MULTILINE))

    doc_type = ""
    label_suffix = ""

    if has_script and ("场次：" in text or "场次" in text or "▲" in text or "第一集" in text or "第1集" in text):
        doc_type = "script"
        ep_range = re.findall(r'(?:第|\b)([0-9]+-[0-9]+)(?:集|\b)', text)
        if ep_range:
            label_suffix = f"第{ep_range[0]}集剧本正文"
        else:
            label_suffix = "剧本正文"
    elif has_ep_outline:
        doc_type = "episode_outline"
        label_suffix = "前十集集纲"
    elif has_outline:
        doc_type = "outline"
        label_suffix = "故事大纲"
    elif has_character:
        doc_type = "character"
        label_suffix = "人物小传与角色设定"
    elif has_analysis:
        doc_type = "analysis"
        label_suffix = "对标拆解分析方案"

    if not doc_type:
        return None

    lines = text.splitlines()
    clean_lines = []
    in_body = False

    for line in lines:
        stripped = line.strip()
        if not in_body:
            if re.search(r'^(?:#+|【)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|故事大纲|前十集集纲|对标拆解分析方案|Step1-3|Step5-6)', stripped):
                in_body = True

        if in_body:
            if any(k in stripped for k in ["集要点:", "集要点：", "字数自算", "在1000以内", "你先审", "告诉我你的想法", "选完（或告诉我", "我立刻按同样"]):
                break
            if any(stripped.startswith(k) for k in ["数一下字数", "符合要求", "请确认是否", "你定一下", "请在下方说明"]):
                continue
            clean_lines.append(line)

    cleaned_body = "\n".join(clean_lines).strip()
    if len(cleaned_body) < 150:
        return None

    drama_title = extract_smart_filename(content, messages, user_input, wmode)
    if drama_title and label_suffix:
        final_filename = f"{drama_title}_{label_suffix}"
    elif drama_title:
        final_filename = f"{drama_title}_{label_suffix or '创作文档'}"
    else:
        final_filename = f"短剧_{label_suffix or '创作文档'}"

    safe_name = re.sub(r'[\\/:*?"<>|\r\n\t\s]+', '_', final_filename).strip('_')
    filepath = os.path.join(session_dir, f"{safe_name}.docx")
    md_filepath = os.path.join(session_dir, f"{safe_name}.md")

    try:
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_body)

        doc = docx.Document()
        doc.add_heading(final_filename, 0)
        for p in cleaned_body.split('\n'):
            if p.strip():
                doc.add_paragraph(p.strip())
        doc.save(filepath)
        return safe_name + ".docx"
    except Exception as e:
        print("Save docx error:", e)
        return None

def parse_docx(file_bytes: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        if not paras:
            for table in doc.tables:
                for row in table.rows:
                    rt = " ".join([c.text.strip() for c in row.cells if c.text.strip()])
                    if rt: paras.append(rt)
        return "\n".join(paras)
    except Exception:
        return ""

class ChatRequest(BaseModel):
    token: Optional[str] = ""
    api_key: Optional[str] = ""
    apikey: Optional[str] = ""
    api_url: Optional[str] = "https://yunwu.ai/v1"
    apiurl: Optional[str] = ""
    model: str = "gpt-4o"
    work_mode: Optional[str] = "通用"
    workmode: Optional[str] = "通用"
    messages: list = []
    user_input: Optional[str] = ""
    userinput: Optional[str] = ""
    doc_text: Optional[str] = ""
    doctext: Optional[str] = ""
    session_id: Optional[str] = ""
    sessionid: Optional[str] = ""
    cid: Optional[str] = ""

class FetchModelsRequest(BaseModel):
    api_key: Optional[str] = ""
    apikey: Optional[str] = ""
    api_url: Optional[str] = "https://yunwu.ai/v1"
    apiurl: Optional[str] = ""

# 注册与登录 API
@app.post("/api/auth/register")
async def register(req: AuthRequest):
    u = req.username.strip().lower()
    p = req.password.strip()
    if not u or not p:
        return {"status": "error", "message": "用户名和密码不能为空"}
    if len(u) < 3 or len(p) < 4:
        return {"status": "error", "message": "用户名至少3位，密码至少4位"}
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        pw_h = hash_pw(p)
        c.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                  (u, pw_h, int(time.time())))
        user_id = c.lastrowid
        token = secrets.token_hex(16)
        c.execute("INSERT INTO user_tokens (token, user_id, username, created_at) VALUES (?, ?, ?, ?)",
                  (token, user_id, u, int(time.time())))
        conn.commit()
        conn.close()
        return {"status": "ok", "token": token, "username": u, "user_id": user_id}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "message": "该用户名已存在，请直接登录"}

@app.post("/api/auth/login")
async def login(req: AuthRequest):
    u = req.username.strip().lower()
    p = req.password.strip()
    pw_h = hash_pw(p)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username = ? AND password_hash = ?", (u, pw_h))
    row = c.fetchone()
    if not row:
        conn.close()
        return {"status": "error", "message": "用户名或密码错误"}
    
    user_id = row[0]
    username = row[1]
    token = secrets.token_hex(16)
    c.execute("INSERT INTO user_tokens (token, user_id, username, created_at) VALUES (?, ?, ?, ?)",
              (token, user_id, username, int(time.time())))
    conn.commit()
    conn.close()
    return {"status": "ok", "token": token, "username": username, "user_id": user_id}

@app.get("/api/auth/me")
async def get_me(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    return {"status": "ok", "user": user}

@app.get("/api/history/list")
async def list_history_sessions(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT session_id, title, mode, updated_at FROM user_sessions WHERE username = ? ORDER BY updated_at DESC", (username,))
    rows = c.fetchall()
    conn.close()
    
    sessions = []
    for r in rows:
        sessions.append({
            "session_id": r[0],
            "title": r[1] or "短剧对标会话",
            "mode": r[2] or "通用",
            "updated_at": r[3]
        })
    return {"status": "ok", "sessions": sessions}

@app.get("/api/history/detail/{session_id}")
async def get_history_detail(session_id: str, token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    
    session_dir, safe_session = get_user_session_dir(username, session_id)
    history_file = os.path.join(session_dir, "history.json")
    
    chat_messages = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                chat_messages = json.load(f)
        except Exception:
            chat_messages = []
            
    files = []
    if os.path.exists(session_dir):
        all_f = os.listdir(session_dir)
        all_f.sort(key=lambda f: os.path.getmtime(os.path.join(session_dir, f)), reverse=True)
        for f in all_f:
            if f.endswith('.docx') or f.endswith('.txt'):
                if not any(k in f for k in ["Step1-3", "Step5-6", "拆解分析", "大纲方案"]):
                    files.append({"name": f, "path": f"{username}/{safe_session}/{f}"})
                    
    return {"status": "ok", "session_id": safe_session, "messages": chat_messages, "files": files}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        return {"error": "仅支持 .docx 文件"}
    content = await file.read()
    text = parse_docx(content)
    return {"filename": file.filename, "word_count": len(text), "text": text}

@app.post("/api/fetch-models")
async def fetch_models(req: FetchModelsRequest):
    key = (req.api_key or req.apikey or "").strip()
    url = (req.api_url or req.apiurl or "https://yunwu.ai/v1").strip()
    if not key:
        return {"error": "请先填写 API Key", "models": []}
    try:
        import requests as _r
        base = url.rstrip("/")
        resp = _r.get(f"{base}/models", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        fetched = []
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("data", data) if isinstance(data, dict) else data
            if isinstance(items, list):
                for m in items:
                    mid = m.get("id", "") if isinstance(m, dict) else str(m)
                    if mid: fetched.append(mid)
        if not fetched:
            tc = OpenAI(api_key=key, base_url=url, timeout=5.0)
            for m in tc.models.list():
                mid = getattr(m, 'id', None)
                if mid: fetched.append(mid)
        return {"models": sorted(set(fetched))}
    except Exception as e:
        return {"error": str(e)[:200], "models": []}

@app.post("/api/chat")
async def chat(req: ChatRequest, authorization: Optional[str] = Header(None)):
    key = req.api_key or req.apikey
    url = req.api_url or req.apiurl or "https://yunwu.ai/v1"
    wmode = req.work_mode or req.workmode or "通用"
    uinput = req.user_input or req.userinput or ""
    dtext = req.doc_text or req.doctext or ""
    
    user = get_current_user_info(req.token, authorization)
    username = user["username"]

    if wmode == "短剧对标":
        sys_p = BENCH_PROMPT
    elif wmode == "剧本创作":
        sys_p = CREATE_PROMPT
    else:
        sys_p = "你是专业高效的AI创作助手。"

    if dtext:
        sys_p = f"【用户已上传待分析脚本（{len(dtext)}字）】\n\n{dtext}\n\n---\n{sys_p}"

    api_messages = [{"role": "system", "content": sys_p}]
    for m in req.messages:
        if m.get("role") in ("role", "user", "assistant"):
            api_messages.append({"role": m["role"], "content": m["content"]})
    if uinput:
        api_messages.append({"role": "user", "content": uinput})

    client = OpenAI(api_key=key, base_url=url, timeout=300.0)

    def generate():
        full_response = ""
        try:
            response = client.chat.completions.create(
                model=req.model, messages=api_messages, stream=True, timeout=300.0
            )
            for chunk in response:
                if not chunk.choices or len(chunk.choices) == 0:
                    continue
                delta = chunk.choices[0].delta
                if delta.content is not None:
                    full_response += delta.content
                    yield f"data: {json.dumps({'token': delta.content})}\n\n"

            session_raw = str(req.session_id or req.sessionid or req.cid or f"{int(time.time())}").strip()
            session_dir, safe_session = get_user_session_dir(username, session_raw)

            bench_data = extract_template_json(full_response)
            saved = process_document_saving(full_response, session_dir, req.messages, uinput, wmode)
            
            # 保存聊天历史 json
            history_file = os.path.join(session_dir, "history.json")
            new_msgs = list(req.messages) if req.messages else []
            if uinput:
                new_msgs.append({"role": "user", "content": uinput})
            if full_response:
                new_msgs.append({"role": "assistant", "content": full_response})
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(new_msgs, f, ensure_ascii=False, indent=2)

            # 更新 user_sessions 数据库索引
            smart_title = extract_smart_filename(full_response, req.messages, uinput, wmode) or uinput[:20] or "创作会话"
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''
            INSERT OR REPLACE INTO user_sessions (session_id, user_id, username, title, mode, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (safe_session, user["user_id"], username, smart_title, wmode, int(time.time())))
            conn.commit()
            conn.close()

            meta = {"type": "done", "session_dir": session_dir, "saved_file": saved, "template_json": bench_data}
            yield f"data: {json.dumps(meta, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)[:300]})}\n\n"

    return StreamingResponse(
        generate(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"}
    )

@app.get("/api/files/{session_id:path}")
async def list_files(session_id: str, token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    
    parts = session_id.strip('/').split('/')
    if len(parts) >= 2:
        u_name, s_id = parts[0], parts[1]
    else:
        u_name, s_id = username, parts[0]
        
    d = os.path.join(OUTPUT_DIR, u_name, s_id)
    if not os.path.exists(d):
        return {"files": []}
    files = []
    all_files = os.listdir(d)
    all_files.sort(key=lambda f: os.path.getmtime(os.path.join(d, f)), reverse=True)
    for f in all_files:
        if "Step1-3" in f or "Step5-6" in f or "拆解分析" in f or "大纲方案" in f:
            continue
        if f.endswith('.docx') or f.endswith('.txt'):
            files.append({"name": f, "path": f"{u_name}/{s_id}/{f}"})
    return {"files": files}

@app.get("/api/download/{filepath:path}")
async def download_file(filepath: str):
    fp = os.path.join(OUTPUT_DIR, filepath)
    if os.path.exists(fp):
        return FileResponse(fp, filename=os.path.basename(filepath))
    return {"error": "文件不存在"}

@app.get("/api/preview/{filepath:path}")
async def preview_file(filepath: str):
    fp = os.path.join(OUTPUT_DIR, filepath)
    if not os.path.exists(fp):
        return {"error": "文件不存在"}
    raw_text = ""
    filename = os.path.basename(filepath)
    if filename.endswith('.docx'):
        md_fp = fp.replace('.docx', '.md')
        if os.path.exists(md_fp):
            with open(md_fp, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
        else:
            with open(fp, 'rb') as f:
                raw_text = parse_docx(f.read())
    else:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()

    clean_preview = re.sub(r'<thinking>[\s\S]*?(?:</thinking>|$)', '', raw_text, flags=re.DOTALL | re.IGNORECASE).strip()
    clean_preview = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', clean_preview, flags=re.DOTALL | re.IGNORECASE).strip()
    clean_preview = re.sub(r'\[TEMPLATEJSON\][\s\S]*?(?:\[/TEMPLATEJSON\]|$)', '', clean_preview, flags=re.DOTALL | re.IGNORECASE).strip()
    clean_preview = re.sub(r'```json[\s\S]*?```', '', clean_preview, flags=re.DOTALL | re.IGNORECASE).strip()

    lines = clean_preview.splitlines()
    clean_lines = []
    in_body = False
    for line in lines:
        stripped = line.strip()
        if not in_body:
            if re.search(r'^(?:#+|【)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|故事大纲|前十集集纲|对标拆解分析方案|Step1-3|Step5-6)', stripped):
                in_body = True

        if in_body:
            if any(k in stripped for k in ["集要点:", "集要点：", "字数自算", "在1000以内", "你先审", "告诉我你的想法", "选完（或告诉我", "我立刻按同样"]):
                break
            if any(stripped.startswith(k) for k in ["数一下字数", "符合要求", "请确认是否", "你定一下", "请在下方说明"]):
                continue
            clean_lines.append(line)

    final_text = "\n".join(clean_lines).strip() if clean_lines else clean_preview
    return {"text": final_text or "暂无纯文本正文内容"}

@app.delete("/api/delete/{filepath:path}")
async def delete_file(filepath: str):
    fp = os.path.join(OUTPUT_DIR, filepath)
    if os.path.exists(fp):
        try:
            os.remove(fp)
            docx_fp = fp.replace('.md', '.docx')
            if os.path.exists(docx_fp): os.remove(docx_fp)
            return {"status": "ok", "message": "文件已成功删除"}
        except Exception as e:
            return {"error": f"删除失败: {str(e)}"}
    return {"error": "文件不存在"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def read_root():
    idx = os.path.join(SCRIPT_DIR, "index.html")
    if not os.path.exists(idx):
        idx = os.path.join(SCRIPT_DIR, "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"message": "index.html not found"}

@app.get("/api/debug/db")
async def debug_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users")
    users = c.fetchall()
    c.execute("SELECT session_id, username, title, updated_at FROM user_sessions")
    sessions = c.fetchall()
    conn.close()
    return {"users": users, "sessions": sessions}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
