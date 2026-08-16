import os
import sys
import json
import ssl
import base64
import subprocess
import urllib.request
import urllib.parse
import asyncio
import sqlite3
import hashlib
import secrets
import time
import shutil
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, Query, HTTPException, Request, Header
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import imageio_ffmpeg
import cv2

app = FastAPI(title="Video Script Generator FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRATCH_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 共享数据库路径
DB_PATH = os.path.join(os.path.dirname(SCRATCH_DIR), "短剧对标", "database.db")
if not os.path.exists(os.path.dirname(DB_PATH)):
    DB_PATH = os.path.join(SCRATCH_DIR, "database.db")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ctx = ssl._create_unverified_context()

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
    CREATE TABLE IF NOT EXISTS baben_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        video_name TEXT NOT NULL,
        script_text TEXT NOT NULL,
        created_at INTEGER
    )
    ''')
    conn.commit()

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

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "FastAPI local backend server is active!"}

@app.post("/api/auth/register")
async def register(req: AuthRequest):
    u = req.username.strip().lower()
    p = req.password.strip()
    if not u or not p:
        return {"status": "error", "message": "用户名和密码不能为空"}
    
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

@app.get("/api/baben/history/list")
async def list_baben_history(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, video_name, created_at FROM baben_history WHERE username = ? ORDER BY id DESC", (username,))
    rows = c.fetchall()
    conn.close()
    
    records = []
    for r in rows:
        records.append({
            "id": r[0],
            "video_name": r[1],
            "created_at": r[2]
        })
    return {"status": "ok", "records": records}

@app.get("/api/baben/history/detail/{history_id}")
async def get_baben_history_detail(history_id: int, token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, video_name, script_text, created_at FROM baben_history WHERE id = ? AND username = ?", (history_id, username))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return {"status": "error", "message": "该扒本记录不存在或无权限访问"}
    
    return {
        "status": "ok",
        "id": row[0],
        "video_name": row[1],
        "script_text": row[2],
        "created_at": row[3]
    }

@app.get("/api/models")
async def get_models(base_url: str = Query("https://yunwu.ai"), api_key: str = Query("")):
    clean_base_url = base_url.rstrip("/")
    try:
        req_url = f"{clean_base_url}/v1/models" if not clean_base_url.endswith("/v1") else f"{clean_base_url}/models"
        req = urllib.request.Request(req_url, headers={"Authorization": f"Bearer {api_key}"})
        res = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(res.read().decode('utf-8'))
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload_and_analyze")
async def upload_and_analyze(
    video: UploadFile = File(...),
    token: Optional[str] = Form(None),
    authorization: Optional[str] = Header(None),
    base_url: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    no_slice: Optional[str] = Form(None),
    episode_num: Optional[str] = Form(None),
    prev_characters: Optional[str] = Form(None),
    prev_context: Optional[str] = Form(None)
):
    user = get_current_user_info(token, authorization)
    
    # Task UUID 独立目录隔离，解决并发竞争覆盖！
    task_id = secrets.token_hex(6)
    task_dir = os.path.join(SCRATCH_DIR, f"task_{task_id}")
    os.makedirs(task_dir, exist_ok=True)
    
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    saved_path = os.path.join(task_dir, f"input_video{ext}")
    
    contents = await video.read()
    with open(saved_path, "wb") as f:
        f.write(contents)

    clean_base_url = (base_url or "https://yunwu.ai").rstrip("/")
    clean_api_key = api_key or ""
    clean_model = model or "gemini-3.1-pro-preview"
    clean_prompt = prompt or ""
    is_no_slice = (str(no_slice or "true").lower() in ["true", "1", "yes"])
    ep_num_str = str(episode_num or "1")
    ep_num = int(ep_num_str) if ep_num_str.isdigit() else 1
    clean_prev_chars = prev_characters or ""
    clean_prev_ctx = prev_context or ""

    return StreamingResponse(
        stream_fast_timeout_pipeline(user, video.filename, saved_path, task_dir, clean_base_url, clean_api_key, clean_model, clean_prompt, is_no_slice, ep_num, clean_prev_chars, clean_prev_ctx),
        media_type="text/event-stream"
    )

def clean_and_merge_script(script_text: str) -> str:
    if not script_text:
        return ""
    
    cleaned = re.sub(r'第X集X-?', '', script_text)
    cleaned = re.sub(r'^(\d+-\d+)[、,，]\s*', r'\1 ', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^▲[.\s、]+', r'▲ ', cleaned, flags=re.MULTILINE)
    
    cleaned = re.sub(r'，?倒吸一口?凉气', '', cleaned)
    cleaned = re.sub(r'倒吸一口?凉气，?', '', cleaned)
    cleaned = re.sub(r'难以置信地?', '', cleaned)
    cleaned = re.sub(r'，?在一旁瞪大双眼', '', cleaned)
    cleaned = re.sub(r'瞪大双眼，?', '', cleaned)
    cleaned = re.sub(r'[（\(]平静[）\)]', '（点头）', cleaned)
    
    lines = [l.strip() for l in cleaned.split('\n') if l.strip()]
    processed_lines = []
    
    for l in lines:
        if '：' in l or ':' in l:
            parts = re.split(r'([:：])', l, maxsplit=1)
            if len(parts) == 3:
                speaker_part = parts[0]
                sep = parts[1]
                dialogue_part = parts[2]
                
                inner_bracket_match = re.search(r'(.+?)[（\(]([^）\)]+)[）\)](.+)', dialogue_part)
                if inner_bracket_match:
                    d1 = inner_bracket_match.group(1).strip()
                    inner_emo = inner_bracket_match.group(2).strip()
                    d2 = inner_bracket_match.group(3).strip()
                    clean_speaker = re.sub(r'[（\(][^）\)]+[）\)]', '', speaker_part)
                    processed_lines.append(f"{speaker_part}{sep}{d1}")
                    if d2:
                        processed_lines.append(f"{clean_speaker}（{inner_emo}）：{d2}")
                    continue
                else:
                    processed_lines.append(l)
                    continue
        processed_lines.append(l)
        
    return '\n\n'.join(processed_lines)

async def stream_fast_timeout_pipeline(user: dict, original_video_name: str, file_path: str, task_dir: str, base_url: str, api_key: str, model: str, prompt: str, no_slice: bool = True, episode_num: int = 1, prev_characters: str = "", prev_context: str = ""):
    def send_evt(data_dict):
        return f"data: {json.dumps(data_dict, ensure_ascii=False)}\n\n"

    clean_filename = os.path.splitext(original_video_name)[0]
    yield send_evt({'type': 'progress', 'msg': f'1/4 正在利用 FFmpeg 提取第 {episode_num} 集视频的无损音轨与视频帧...'})
    await asyncio.sleep(0.1)

    audio_path = os.path.join(task_dir, 'full_audio.mp3')
    cmd_audio = f'"{ffmpeg_exe}" -y -i "{file_path}" -vn -acodec libmp3lame -q:a 0 "{audio_path}"'
    subprocess.run(cmd_audio, capture_output=True, encoding='utf-8', errors='ignore', shell=True)

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps if fps else 60.0

    if no_slice:
        chunk_sec = duration_sec
        num_chunks = 1
        yield send_evt({'type': 'progress', 'msg': f'2/4 音画提取完成！全剧 {duration_sec:.1f} 秒，采用【全量直接生成】模式 (不切割切片)...'})
    else:
        chunk_sec = 25.0
        num_chunks = max(1, int(duration_sec // chunk_sec) + (1 if duration_sec % chunk_sec > 3 else 0))
        yield send_evt({'type': 'progress', 'msg': f'2/4 音画提取完成！全剧 {duration_sec:.1f} 秒，拆分为 {num_chunks} 个 AI 分析单元...'})

    await asyncio.sleep(0.1)

    full_script = ""
    last_context_summary = "无（00:00秒开篇第一句）"
    last_scene_no = "1-1"
    global_characters = ""

    for c in range(num_chunks):
        if no_slice:
            start_t = 0.0
            end_t = duration_sec
            frame_count_target = max(1, int(duration_sec))
            yield send_evt({'type': 'progress', 'msg': f'3/4 全量视频发起 AI 解析 (全剧 {duration_sec:.1f}s，严格每秒 1 帧高密抽帧共 {frame_count_target} 帧)...'})
            chunk_audio_path = audio_path
        else:
            start_t = c * chunk_sec
            end_t = min((c + 1) * chunk_sec, duration_sec)
            if start_t >= duration_sec: break
            yield send_evt({'type': 'progress', 'msg': f'3/4 正在拆解第 {c+1}/{num_chunks} 单元 ({start_t:.1f}s ~ {end_t:.1f}s)，正在发起 API 请求...'})
            chunk_audio_path = os.path.join(task_dir, f'chunk_audio_{c+1}.mp3')
            cmd_slice = f'"{ffmpeg_exe}" -y -ss {start_t} -to {end_t} -i "{audio_path}" -acodec copy "{chunk_audio_path}"'
            subprocess.run(cmd_slice, capture_output=True, encoding='utf-8', errors='ignore', shell=True)

        await asyncio.sleep(0.1)

        audio_b64 = ""
        if os.path.exists(chunk_audio_path):
            with open(chunk_audio_path, 'rb') as f:
                audio_b64 = base64.b64encode(f.read()).decode('utf-8')

        stage1_user_contents = []
        if audio_b64:
            stage1_user_contents.append({
                'type': 'input_audio',
                'input_audio': {'data': audio_b64, 'format': 'mp3'}
            })

        frame_step = int(fps) if fps else 30
        curr_frame = int(start_t * fps)
        end_frame_target = int(end_t * fps)

        while curr_frame < end_frame_target:
            cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            ret, frame = cap.read()
            if not ret: break

            sec_current = curr_frame / fps
            m_s = int(sec_current // 60)
            s_s = int(sec_current % 60)
            ts_str = f"{m_s:02d}:{s_s:02d}"

            h, w = frame.shape[:2]
            max_dim = 1280
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            img_b64 = base64.b64encode(buffer).decode('utf-8')
            img_url = f"data:image/jpeg;base64,{img_b64}"

            stage1_user_contents.append({'type': 'text', 'text': f'【时间戳 {ts_str}】'})
            stage1_user_contents.append({'type': 'image_url', 'image_url': {'url': img_url}})
            curr_frame += frame_step

        stage1_system_prompt = prompt or "你是专业影视拉片师，请严格 1:1 还原剧本。"
        
        chat_url = f"{base_url}/chat/completions" if base_url.endswith("/v1") else f"{base_url}/v1/chat/completions"
        stage1_payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': stage1_system_prompt},
                {'role': 'user', 'content': stage1_user_contents}
            ],
            'temperature': 0.1,
            'max_tokens': 16384
        }

        stage1_raw_text = ""
        try:
            req = urllib.request.Request(chat_url, data=json.dumps(stage1_payload).encode('utf-8'), headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
            res = urllib.request.urlopen(req, timeout=300, context=ctx)
            data = json.loads(res.read().decode('utf-8'))
            stage1_raw_text = data['choices'][0]['message']['content']
        except Exception as e:
            yield send_evt({'type': 'error', 'message': f'第 {c+1} 单元识别失败: {str(e)}'})
            cap.release()
            shutil.rmtree(task_dir, ignore_errors=True)
            return

        stage2_system_prompt = "你是专业短剧编剧，请整理润色为高品质剧本正文。"
        stage2_user_contents = [{'type': 'text', 'text': f'原剧本草稿:\n{stage1_raw_text}'}]

        if audio_b64:
            stage2_user_contents.append({
                'type': 'input_audio',
                'input_audio': {'data': audio_b64, 'format': 'mp3'}
            })

        cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_t * fps))
        sample_step = int(fps * 2)
        curr_frame_s2 = int(start_t * fps)
        while curr_frame_s2 < end_frame_target:
            cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_s2)
            ret, frame = cap.read()
            if not ret: break

            sec_c = curr_frame_s2 / fps
            ts = f"{int(sec_c // 60):02d}:{int(sec_c % 60):02d}"
            h, w = frame.shape[:2]
            if max(h, w) > 1280:
                scale = 1280 / max(h, w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            _, buf = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            img_url = f"data:image/jpeg;base64,{base64.b64encode(buf).decode('utf-8')}"
            stage2_user_contents.append({'type': 'text', 'text': f'【时间戳 {ts}】'})
            stage2_user_contents.append({'type': 'image_url', 'image_url': {'url': img_url}})
            curr_frame_s2 += sample_step

        stage2_payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': stage2_system_prompt},
                {'role': 'user', 'content': stage2_user_contents}
            ],
            'temperature': 0.0,
            'max_tokens': 16384
        }

        chunk_script = ""
        for attempt in range(2):
            try:
                req = urllib.request.Request(chat_url, data=json.dumps(stage2_payload).encode('utf-8'), headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                })
                res = urllib.request.urlopen(req, timeout=120, context=ctx)
                data = json.loads(res.read().decode('utf-8'))
                content = data['choices'][0]['message']['content']
                if content and content.strip():
                    chunk_script = content.strip()
                    break
                else:
                    chunk_script = stage1_raw_text
            except Exception:
                if attempt == 1:
                    chunk_script = stage1_raw_text
                    break

        if chunk_script:
            cleaned_chunk = clean_and_merge_script(chunk_script.strip())
            if full_script and c > 0:
                chunk_lines = cleaned_chunk.split('\n')
                filtered_lines = [l for l in chunk_lines if not (l.strip() == "第1集" or l.strip().startswith("1-1") or l.strip().startswith("人物："))]
                cleaned_chunk = "\n".join(filtered_lines).strip()
                full_script += "\n" + cleaned_chunk
            else:
                full_script = cleaned_chunk

            yield send_evt({'type': 'chunk', 'content': cleaned_chunk, 'chunk_index': c + 1, 'total_chunks': num_chunks})

    cap.release()

    if not full_script or not full_script.strip():
        yield send_evt({'type': 'error', 'message': 'API 接口未返回内容。'})
        shutil.rmtree(task_dir, ignore_errors=True)
        return

    full_script = clean_and_merge_script(full_script)

    # 存储到该用户专属隔离目录与数据库
    username = user["username"]
    user_out_dir = os.path.join(OUTPUT_DIR, username)
    os.makedirs(user_out_dir, exist_ok=True)
    out_file = os.path.join(user_out_dir, f"{clean_filename}_1对1零删减全量剧本.txt")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(full_script)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO baben_history (user_id, username, video_name, script_text, created_at) VALUES (?, ?, ?, ?, ?)",
              (user["user_id"], username, clean_filename, full_script, int(time.time())))
    conn.commit()
    conn.close()

    # 清理任务临时临时目录
    shutil.rmtree(task_dir, ignore_errors=True)

    yield send_evt({'type': 'done', 'full_script': full_script, 'file_saved': out_file})

app.mount("/", StaticFiles(directory=SCRATCH_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
