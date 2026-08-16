import sqlite3, os, hashlib, secrets, time

db_path = r'C:\Users\Administrator\Desktop\短剧对标\test_user_db.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
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

conn.commit()

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(username, password):
    username = username.strip().lower()
    if not username or not password:
        return None, "用户名和密码不能为空"
    pw_h = hash_pw(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                  (username, pw_h, int(time.time())))
        conn.commit()
        return login(username, password)
    except sqlite3.IntegrityError:
        return None, "该用户名已被注册"

def login(username, password):
    username = username.strip().lower()
    pw_h = hash_pw(password)
    c.execute("SELECT id, username FROM users WHERE username = ? AND password_hash = ?", (username, pw_h))
    user = c.fetchone()
    if not user:
        return None, "用户名或密码错误"
    
    token = secrets.token_hex(16)
    c.execute("INSERT INTO user_tokens (token, user_id, username, created_at) VALUES (?, ?, ?, ?)",
              (token, user[0], user[1], int(time.time())))
    conn.commit()
    return {"token": token, "username": user[1], "user_id": user[0]}, None

u1, err = register("test_user_1", "pass123")
print("Register 1:", u1, err)

u2, err = register("test_user_2", "pass456")
print("Register 2:", u2, err)

u1_login, err = login("test_user_1", "pass123")
print("Login 1:", u1_login, err)

conn.close()
os.remove(db_path)
