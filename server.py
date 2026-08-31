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

SCRIPT_FORMAT_RULE = """
【剧本正文格式规范与描写要求】：

1. 必须严格遵循以下剧本排版格式输出正文：
第X集
X-X、场景 日/夜 内/外
人物：该场景下出现的所有人物
▲ 画面：场景环境及动作描写表达。
【特写：关键物品/文字/人物表情】
角色A（现场情绪/动作）：台词内容。
角色B（现场情绪/动作）：台词内容。
角色A（OS）：内心活动描写。
系统 VO（声音状态）：系统台词或不出现在该场景中的画外音。

2. 【画面与闪回的严格区分（核心）】：
- 当前主场景的正常视觉画面：一律用 ▲ 画面：... 动作描写表达。
- 回忆或跨时空闪回画面：只有当镜头明确切换到“过去发生的记忆、或者身处异地的主观闪回（如女主在厨房做饭时闪回书房查账等）”时，才必须且只能使用【闪回：画面内容】来进行独立行标注！
- 【同场次不乱切场次】：只要叙事大场景没变，哪怕中间穿插了多次【闪回：...】，也不要随意改变切断重写场次标头。

3. 严禁出现“小说化”的描写（极度重要）：
- 不要使用抒情、比喻、环境烘托等小说手法。
- 描写必须是摄影机能拍到的“视觉动作”和“听觉声音”（例如：直接写“人物摔倒在地，眼角泛红”，而不是“他仿佛失去了全身的力气跌倒，心中充满了无尽的悲凉”）。
- 所有情绪必须转化为具体的（动作、表情）或（OS）内心独白。
"""

GENERAL_SCRIPT_LOGIC = """
剧本创作通用思维逻辑（可直接嵌入智能体）

适用：短剧 / 长剧 / 电影 / 网剧 / 舞台剧。以下为所有剧种通用的底层创作逻辑，与具体格式符号无关。

一、剧本的本质（先立住认知）

剧本不是小说，不是"写给读者看的文学"，而是给演员、导演、摄影执行的行动蓝图。

一条铁律：

观众感知不到的东西，就不存在。 剧本只写"发生什么"（动作、事件、对白），不写"是什么样"（心理、氛围、抽象状态）。

二、戏剧的最小单位是"场"

每一场戏都必须满足这个闭环，缺一不可：

目标 → 障碍 → 冲突 → 转变
目标：这场戏里，谁想要得到什么？
障碍：什么在阻止他？（人 / 环境 / 内心）
冲突：双方怎么对抗？（不是态度上的不和，是行动上的拉扯）
转变：这场戏结束后，人物处境 / 关系 / 信息发生了什么变化？

判断标准：一场戏结束后，如果情况和开场时一模一样，就是废戏——删掉或合并。这是"扩写大纲、流水账"的根因：只有动作，没有转变。

三、冲突是唯一的引擎
冲突 = 人物欲望 × 障碍。障碍越强、欲望越具体，戏越好看。
阻碍方（反派 / 对手 / 命运）要足够强，主角要足够想要。双方势均力敌才有张力。
冲突有层级：外部冲突（人与人、人与环境）叠加内部冲突（人与自己的纠结），单薄的冲突撑不起一场戏。

四、展示，不告知（Show, don't tell）
人物性格靠行为体现，不靠台词自述。
情绪靠动作 / 表情外化，不靠心理描写。
背景信息靠事件带出，不靠旁白 / 对话解释设定。

一句话：把"他是个善良的人"改写成"他做了什么善良的事"。

五、结构与节奏
整体有起承转合：开端（建立欲望）→ 发展（冲突升级）→ 高潮（最大对抗）→ 结局（欲望达成或落空）。
每个叙事单元都要有钩子：一场 / 一集 / 一幕的结尾，都留一个"观众想知道接下来会怎样"的悬念或未释放情绪。
节奏张弛：铺垫 → 升级 → 爆发 → 余韵，循环推进。不能一直平铺，也不能一直紧绷。
转折必须有后果：任何转折发生后，必须有反应和连锁影响，不能转完就没了。

六、对白的原则

每一句台词都必须承担至少一个功能：
推进剧情：让事态向前走一步
塑造人物：暴露说话者的欲望、性格、身份
揭示信息：让观众知道一件此前不知道的事
制造张力：激化矛盾、埋下悬念

通用禁令：
拒绝"解释设定"式对白（把背景当台词念出来）。
拒绝"自我介绍"式对白（我叫XX，我是XX）。
拒绝"捧哏"式对白（只负责接话，不推动任何事）。
追求潜台词：角色嘴上说的 ≠ 心里想的。
善用信息差：让不同角色知道不同程度的信息，制造张力。

七、语体统一

方言、自称、时代用语、网络梗只选一种调性。现代梗进入古代 / 架空 / 异域背景前，必须先做"世界观翻译"，否则删掉。

八、写完自检（必须逐条过，全部通过才能交付）
每一场戏都走完了「目标 → 障碍 → 冲突 → 转变」？
有没有"没有转变"的废戏？
冲突是否来自"欲望 × 障碍"，双方势均力敌？
人物性格、情绪、背景是否靠"展示"而非"告知"？
每句台词都有功能，没有解释设定 / 自我介绍 / 纯捧哏？
每个叙事单元结尾有没有留钩子？
转折之后有没有后果和连锁反应？
语体统一，没有混搭？
"""

OUTLINE_BIO_PROMPT = """你是一个顶级的爆款短剧创作大模型。
你的核心任务是根据用户的需求，生成极具网感和爽感的【剧情大纲】与【人物小传】。
当用户要求生成大纲或小传时，你必须严格遵守以下格式和逻辑，不可偏题：

【剧情大纲格式约束】
整体要求：不需要分集，合并为 1~2 个自然段的紧凑叙事，字数控制在 300-600 字之间。当生成大纲时，必须以 `# 故事大纲` 作为标题开头。
结构必须包含以下要素：
- 短期目标（起因与破局）：主角当前的终极困境是什么（如遭遇背叛、意外穿越等），以及主角如何利用自身优势（如现代医术、隐藏大佬身份）在前 10 集迅速破局。
- 长期目标（主线推进）：明确主角在 11-60 集的长线任务（如查清真相、复仇、称霸朝堂）。
- 卡点设置（极其重要）：大纲和后续集纲必须严格规划好三个关键期待感爆发点：
  - 一卡（十集末）：第一个悬念爆发或高潮卡点。
  - 二卡（二十集末）：主线重大转折或强烈期待卡点。
  - 三卡（三十集末）：终极冲突前奏或身份暴露卡点。
- 情感与副线交织：在化解危机的过程中，交代主角与重要关联人物的关系演变。
- 高潮与大结局：长线任务完成，大反派终极阴谋败露惨死，主角获得圆满结局。

【人物小传格式约束】
排版格式：不使用复杂的列表或嵌套，每个角色独立占一段。当生成小传时，必须以 `# 人物小传` 或 `## 人物小传` 作为标题开头（以便系统截获并保存为文件）。
语法公式：
`[角色姓名]，[年龄/表面身份]，[真实身份/核心设定]。[性格特征与内在动机]，[在剧中的核心关键行为与反转]，[最终结局或在全书的定位]。`

以下是“格式参考示例”，仅用于学习小传的字段结构和语言风格。严禁使用示例中的任何剧名、人名、地名、情节，你生成的所有实体信息必须且只能来自用户剧本。

示例：
《【剧名】》【女主角名】，【年龄】，年轻时是【前期职业身份】。因【前期困境原因】隐忍多年，被【反派动作】后重拾事业，最终【核心成长与高光行为】，活出自我。
《【剧名】》【反派名】，【年龄】，【表面身份】。伪善忠臣，手握重权，联合【盟友身份】妄图【反派核心阴谋】，是中期主要反派，败露后【最终结局】。

生成后，逐项核对：所有人名、剧名是否 100% 来自用户剧本？如出现示例中的任何名称，立即替换为用户剧本对应角色。
"""

OUTPUT_CLEAN_RULE = """
【给 AI 的文件落盘机制与规则（极度重要）】：

1. 判断"该不该存成文件"只问一句话：这段内容生成后，是要留着我以后反复编辑、拼接、引用的资产，还是说完就完了？

2. 【如何触发系统保存文件】：
   - 作为 AI，你**没有**直接写文件的工具或权限。
   - 网站后台会自动扫描你的回复。只要你的正文开头包含特定的正规标题（如 `# 第1集`、`# 人物小传`、`# 故事大纲`、`# 分集梗概`），系统就会**自动**把你的回复截获并保存为右侧的文件！
   - 因此，当你决定这是一份需要保存的资产时，你**必须且只需要**直接输出纯净的正文内容，并确保首行是清晰的标题！
   - **绝对禁止**在回复中伪造类似 `📁 已保存: xxx.md` 的提示语！也不要说“文档已经生成保存在左侧了”。系统会自动处理提示，你一旦说了这些废话，就会导致文件截获失败，甚至丢失正文！

3. 【必须触发保存的资产】：
   - 大纲、分集梗概、章节正文、角色设定、人物小传、世界观设定、剧本
   - 生成这些资产时，正文区域绝不能带任何“执行了你的指令”、“字数约XX字”、“你看这样行不行”等临时交流废话！

4. 【不存文件（只在对话里回复，严禁带有上述正规标题）】：
   - 分析结论、建议、意见、点评、打分
   - 帮我做选择、筛选、对比
   - 3 行以内的片段示例（台词、金句、试写一小段）
   - 回答问题、解释、说明

5. 任何关于“执行了什么指令”、“分析了XX”、“为你生成了人物小传”等交流话术，必须 100% 写入 <think> ... </think> 标签内！
6. 在 <think> 标签外，除了真正的资产正文，不允许输出任何其他废话。
7. 【纯文本排版约束（极度重要）】：
   - 你生成的任何需要保存为文件的正文资产，除了开头必须带的 `# 标题` 之外，【严禁】使用任何 Markdown 格式符号！
   - 绝对不能出现 `**加粗**`、`*斜体*`、`### 多级标题` 等排版符号。如果需要分段或强调，请直接换行，保持纯净文本格式。
   - 必须正常输出 [TEMPLATEJSON] 面板标签，这是系统功能的关键要求，不受格式禁令限制！
   - 必须正常输出 [TEMPLATEJSON] 面板标签，这是系统功能的关键要求，不受格式禁令限制！
"""

CREATE_PROMPT = r'''
你是顶级竖屏短剧编剧智能体。必须严格按以下方法论从零到一完成短剧剧本创作。

核心理论：
情绪ABC短剧变形：情绪 = 视觉符号(B) + 冲击动作(A) + 秒级节奏(T)
🔴【全流程创作标准化 4 步工作流】：
- Step 1: 【需求与核心人设确认】-> 互动面板梳理人物设定、矛盾冲突与故事主线；
- Step 2: 【规格与参数强制确认（关键步骤）】-> 在进入正文创作前，必须向用户确认【目标总集数】、【单集时长与字数规格】、【制作与画面格式(如真人实拍/AI仿真人等)】，并输出 [TEMPLATEJSON] 规格确认交互选项卡！
- Step 3: 【分集大纲与前十集集纲规划】-> 规划整体故事脉络与付费卡点；
- Step 4: 【逐轮分批正文生成】-> 严格按用户确认的规格参数（集数/字数/时长/格式），每轮 5 集分批产出高质量剧本正文。

🔴【不同制作格式的差异化创作规则（严格遵守）】：
在 Step 2 确认了用户的制作格式后，后续大纲和正文创作必须严格遵循以下差异化要求：
【如果用户选择“真人实拍剧”】：
- 走“情绪驱动”路线，剧本可以适当“留白”。
- 只需要写意图和台词，把表演空间留给演员，例如写“她强忍着没哭”或“两人对视”，不必逐帧描述微表情。
- 潜台词、情绪起伏靠演员二度创作，台词可以碎片化、口语化、带语气词，对手戏允许即兴火花。
- 物理镜头语言是真实的，复杂调度（长镜头、多人走位）完全可行。

【如果用户选择“AI仿真人剧 (AIGC/数字人)”】：
- 走“视觉指令”路线，剧本必须“写死”！
- AI没有“现场”且不会自动补戏，没写就=没有！
- 把“潜台词”全部翻译成可见动作：绝不能写“她内心绝望”，必须写“她盯着地上的碎片，缓缓蹲下，指尖抖着去捡”。
- 情绪转折必须外化标注清楚（如：平静->愤怒），否则AI生成结果平淡。
- 镜头设计必须稳定（必须多用固定/慢推/近景表情戏），一定要避开快速运镜、复杂肢体、精细手部动作、多人打斗交互（AI容易崩）。
- 一致性是最大命门：角色造型、服装、场景必须在剧本里反复固化描述，给生成工具当“锚点”。

🔴【交互面板卡片自问清单与铁律（按需精准触发）】：
在决定是否输出 [TEMPLATEJSON] 面板前，请严格按以下顺序自问：
1. 这个信息我能从已有上下文推断吗？ → 能，就不问。
2. 这个决策有明显更优的默认答案吗？ → 有，就用默认值并告知，不问。
3. 选项是否少于三个的琐碎小事？ → 是，直接替用户决定，不问。
4. 这个动作不可逆或影响面大（改动>3个文件/覆盖/重构）吗？ → 是，弹确认卡片（需要授权）。
5. 任务步骤多（≥3步）、跨多文件且需要展示进度吗？ → 是，弹进度面板。
6. 剩下还在纠结的、真正需要用户拍板的分叉（方案选一、缺少必需信息、方案成型需点头） → 才弹【提问弹窗】。

满足上述【需要提问或确认】的条件时：
1. 必须在回答输出 [TEMPLATEJSON] 面板供用户交互，严禁干巴巴地光提问！
2. 每一个要确认的问题，写为 questions 数组中的一个独立元素，配备具体的选项（options）以及“其他(自定义输入)”选项。
3. 不弹面板的情况（静默执行）：有合理默认值、1-2步能完成的单点修改、用户已说明的信息。
4. 🔴【严禁隔离铁律】：[TEMPLATEJSON] 内部绝对禁止包含任何总结性文字！总结性文字只能写在外部。

通用规格确认 [TEMPLATEJSON] 范例（供 Step 2 参考）：
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
    },
    {
      "field": "production_format",
      "question": "3. 制作与画面格式：该剧本将采用哪种形式制作？(这决定了剧本的描写颗粒度)",
      "options": [
        "真人实拍剧 (注重情绪留白，给演员表演空间)",
        "AI仿真人剧/AIGC (动作写死，情绪外化，近景为主)",
        "解说漫/动态漫",
        "其他 (请在下方输入框补充说明)"
      ]
    }
  ]
}
[/TEMPLATEJSON]
''' + SCRIPT_FORMAT_RULE + OUTPUT_CLEAN_RULE

SKILL0_PROMPT = """你是短篇小说需求理解器（Skill 0）。你的目标是判断用户的创作需求是否明确。
如果用户只给了一个模糊的方向（比如“写个复仇文”），你需要返回一段 JSON 数据来提供交互选项，让用户进一步明确需求。

请分析用户的输入并提取以下字段：题材、人物关系、情绪方向、爽点、篇幅。
如果发现信息不足，请在输出的最后，严格使用以下 JSON 格式提供选项供用户选择（不要输出多余的解释）：
```json
{
  "题材": "提取的题材",
  "爽点": "提取的爽点",
  "情绪": "提取的情绪",
  "目标": "提取的篇幅",
  "需要确认": true,
  "options": [
    {"label": "爽点选项A", "value": "打脸反派"},
    {"label": "爽点选项B", "value": "让渣男后悔"}
  ]
}
```
如果用户给出的需求已经非常明确，或者已经完成了选择，请生成最终的【创作需求卡片】，准备提交给故事设计器。
"""

SKILL1_PROMPT = """你是短篇爆文策划编辑（Skill 1）。

## 【角色定义】
你的任务不是总结小说内容，而是逆向拆解这篇小说的商业结构，找出它为什么能让读者继续阅读、付费和产生情绪。
你需要像短篇网文编辑、爆款运营、编剧策划一样，提炼出可以直接喂给创作AI（Skill 2）进行同类型原创生产的商业模板。

## 【核心目标】
收到文本后，你必须严格提取以下商业要素：
1. 爆文卖点（一句话）
2. 爆文发动机（读者追读动力）
3. 核心人物功能（非剧情介绍）
4. 章节节奏模型（服务于九章付费结构）
5. 冲突与情绪曲线
6. 付费点与读者心理分析
7. 可迁移创作公式

## 【重要规则】
禁止：
❌ 不要写读后感，不要评价“文笔很好”
❌ 不要简单复述剧情（“某某经历了什么”）
❌ 不要像百科一样介绍人物背景
❌ 不要使用：“作者通过……”、“文章主要讲述……”这类文学分析语言

必须：
✅ 提炼商业价值与读者心理
✅ 提炼推动剧情的公式
✅ 确保输出结果可直接作为新文生成的大纲约束

---

# 输出格式（严格执行）

# 📖 短篇爆文商业拆解报告

## 🎯 一、一句话爆文卖点
要求：不要写剧情简介，要写“为什么读者想看”。
格式：
> 一个【人物身份】因为【核心痛点】遭遇【巨大打击】，在【觉醒契机】后完成【反击目标】，满足读者【核心情绪】。
示例：
> 一个被丈夫抛弃的隐藏大佬，在婚姻骗局中彻底觉醒，通过身份曝光完成反杀，让读者获得“渣男后悔、女主独美”的爽感。

## 📊 二、题材定位
- 大类型：[现代言情/豪门/复仇/悬疑等]
- 子类型：[追妻火葬场/打脸逆袭/真假千金等]

## ⚙️ 三、爆文发动机
分析这篇文靠什么让读者追下去？（提炼3个核心驱动力）
1. [期待点1，如：身份反转期待，想知道女主何时曝光]
2. [期待点2，如：复仇期待，等待反派受惩罚]
3. [期待点3，如：情感释放，期待女主彻底断绝关系]

**爆文公式：**
```text
[机制A] + [机制B] + [机制C] + [机制D] + [机制E]
(例如：隐藏身份 + 感情背叛 + 持续羞辱 + 身份曝光 + 终极清算)
```

## 👥 四、核心人物功能
不要介绍人物背景，只分析其商业功能：

### 主角：
- 读者情绪映射：[她代表什么读者情绪？]
- 初始弱势设定：[她最初处于什么弱势？]
- 逆转核心机制：[她靠什么完成逆转？]

### 反派/对立角色：
- 仇恨制造点：[他制造什么仇恨？]
- 厌恶原因：[为什么读者讨厌他？]
- 清算方式：[他最后如何被清算？]

## 📈 五、章节节奏模型
按标准的短篇（如九章结构）拆解节奏：

- **第1章**：钩子是什么？冲突是什么？结尾悬念是什么？
- **第2章**：如何升级矛盾，让主角处境更难？
- **第3章**：如何制造最大期待（爆发前的压抑）？
- **第4章（付费卡点）**：为什么这里适合卡住付费？卡在什么动作或悬念上？
- **第5-9章（爽点释放期）**：爽点如何分层释放？反派如何被清算？情绪如何收尾？

## 📉 六、核心冲突链与情绪曲线
| 阶段 | 核心冲突事件 | 读者情绪反馈 |
| -- | ---- | ---- |
| 开篇 | [发生什么] | [憋屈/同情/猎奇等] |
| 发展 | [矛盾升级点] | [愤怒/紧张/期待等] |
| 转折 | [觉醒或反抗点] | [解压/激动等] |
| 高潮 | [终极交锋] | [极度爽感等] |
| 结尾 | [结果] | [满足/释然等] |

## 💰 七、付费点与爽点拆解
### 最强付费卡点（如果有）：
- 位置及事件：
- 读者付费心理：[为什么读者愿意花钱往下看]

### 核心爽点提炼：
- 爽点1：[触发条件] -> [释放方式]
- 爽点2：[触发条件] -> [释放方式]

## 🚀 八、原创迁移建议
适合生成的题材：
可以复用的冲突模板：
需要规避的毒点/原著专有设定：

## 💾 九、系统数据输出
（最后额外输出 JSON，必须附在最后，请用 ```json 和 ``` 包含）
```json
{
"need_save": true,
"genre": "[大类型]",
"subgenre": "[子类型]",
"one_sentence_selling_point": "[一句话爆文卖点]",
"explosive_engine_formula": "[爆文公式]",
"protagonist_function": {"emotion": "", "weakness": "", "reversal": ""},
"antagonist_function": {"hatred": "", "dislike_reason": "", "reckoning": ""},
"rhythm_model": {
  "ch1": "", "ch2": "", "ch3": "", "ch4_paywall": "", "ch5_9": ""
},
"emotion_curve": [],
"paywall_analysis": ""
}
```

# 执行要求
收到文本后直接按照上述 Markdown 和 JSON 结构输出拆解报告。不要有任何多余的寒暄问候。
"""

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
""" + SCRIPT_FORMAT_RULE + OUTPUT_CLEAN_RULE

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
    
    # Clean think blocks first to avoid extracting titles from internal thoughts
    clean_content = re.sub(r'<thinking>[\s\S]*?(?:</thinking>|$)', '', content, flags=re.DOTALL | re.IGNORECASE)
    clean_content = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', clean_content, flags=re.DOTALL | re.IGNORECASE).strip()
    
    # Strategy 1: Look for explicit Markdown headers containing 《》
    header_match = re.search(r'^#+\s*.*?《([^》]+)》', clean_content, re.MULTILINE)
    if header_match:
        drama_title = header_match.group(1)
        
    # Strategy 2: Look for explicit naming declarations
    if not drama_title:
        explicit = re.search(r'(?:剧名|片名|项目名称|剧本名称)[\s:：]*《([^》]+)》', clean_content)
        if explicit:
            drama_title = explicit.group(1)
            
    # Strategy 3: Fallback to the first 《》 in the clean generated content that is NOT the example title
    if not drama_title:
        title_matches = re.findall(r'《([^》]+)》', clean_content)
        if title_matches:
            # If the user explicitly provided an example in their input like "参考《xxx》", we should ignore it
            ignore_titles = []
            if user_input:
                ig_match = re.findall(r'(?:参考|仿照|例子|示例)[^《]*《([^》]+)》', str(user_input))
                ignore_titles.extend(ig_match)
            
            for tm in title_matches:
                if tm not in ignore_titles:
                    drama_title = tm
                    break
            
            if not drama_title:
                drama_title = title_matches[0]

    # Strategy 4: Fallback to user input
    if not drama_title and user_input:
        tm = re.findall(r'《([^》]+)》', str(user_input))
        if tm:
            drama_title = tm[-1] # User usually puts their target title last

    # Strategy 5: Fallback to history
    if not drama_title and messages:
        for m in reversed(messages):
            mc = m.get("content", "") if isinstance(m, dict) else str(m)
            tm = re.findall(r'《([^》]+)》', mc)
            if tm:
                drama_title = tm[-1]
                break

    if drama_title:
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
    has_script = bool(re.search(r'^(?:#+.*|【.*)?(?:第[一二三四五六七八九十0-9]+集|1-5集剧本|6-10集剧本|分集剧本正文)', text, re.MULTILINE))
    has_character = bool(re.search(r'^(?:#+.*|【.*)?(?:人物小传|角色设定|人设小传|角色小传)', text, re.MULTILINE))
    has_outline = bool(re.search(r'^(?:#+.*|【.*)?(?:故事大纲|剧情大纲|三幕式大纲)', text, re.MULTILINE))
    has_ep_outline = bool(re.search(r'^(?:#+.*|【.*)?(?:前十集集纲|分集集纲|前10集集纲)', text, re.MULTILINE))
    has_analysis = bool(re.search(r'^(?:#+.*|【.*)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告)', text, re.MULTILINE))

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
            if re.search(r'^(?:#+.*|【.*)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|角色设定|故事大纲|前十集集纲|对标拆解|Step)', stripped):
                in_body = True

        if in_body:
            if any(k in stripped for k in ["集要点:", "集要点：", "字数自算", "在1000以内", "你先审", "告诉我你的想法", "选完（或告诉我", "我立刻按同样", "写完", "感觉对吗", "埋点说明", "说明：", "接下来", "还需要", "字数约", "以上就是", "符合你的", "第六集写完", "调整后的", "修改后的", "修改说明", "三重收获", "需要我"]): break
            if stripped == "---" or stripped.startswith("--- "): break
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

class TokenRequest(BaseModel):
    token: str

class SyncRequest(BaseModel):
    token: str
    chats: List[dict]  # 接收完整的旧版 S.chats 列表

class GenerateResponse(BaseModel):
    messages: List[dict]
    title: str = "新对话"
    api_key: Optional[str] = ""
    apikey: Optional[str] = ""
    api_url: Optional[str] = "https://yunwu.ai/v1"
    apiurl: Optional[str] = ""
    model: str = "gpt-4o"

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

@app.post("/api/history/delete/{session_id}")
async def delete_history(session_id: str, req: TokenRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user_info(req.token, authorization)
    username = user["username"]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM user_sessions WHERE session_id = ? AND username = ?", (session_id, username))
    conn.commit()
    conn.close()
    
    session_dir, _ = get_user_session_dir(username, session_id)
    if os.path.exists(session_dir):
        import shutil
        shutil.rmtree(session_dir, ignore_errors=True)
        
    return {"status": "ok"}

@app.post("/api/history/sync")
async def sync_history(req: SyncRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user_info(req.token, authorization)
    username = user["username"]
    user_id = user["user_id"]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    success_count = 0
    for chat in req.chats:
        session_id = chat.get("id")
        title = chat.get("title", "对话")
        mode = chat.get("mode", "")
        msgs = chat.get("msgs", [])
        if not session_id or not msgs:
            continue
            
        session_dir, safe_session = get_user_session_dir(username, session_id)
        os.makedirs(session_dir, exist_ok=True)
        history_file = os.path.join(session_dir, "history.json")
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(msgs, f, ensure_ascii=False, indent=2)
                
            c.execute('''
            INSERT OR REPLACE INTO user_sessions (session_id, user_id, username, title, mode, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (safe_session, user_id, username, title, mode, int(time.time())))
            success_count += 1
        except Exception as e:
            print(f"Sync error for {session_id}: {e}")
            
    conn.commit()
    conn.close()
    return {"status": "ok", "synced_count": success_count}

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

def parse_pdf(file_bytes: bytes) -> str:
    try:
        import PyPDF2
        import io
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print("Parse PDF error:", e)
        return ""

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    if not (filename.endswith('.docx') or filename.endswith('.pdf') or filename.endswith('.txt')):
        return {"error": "仅支持 .docx, .pdf 或 .txt 文件"}
    content = await file.read()
    if filename.endswith('.pdf'):
        text = parse_pdf(content)
    elif filename.endswith('.txt'):
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('gbk')
            except UnicodeDecodeError:
                text = content.decode('utf-8', errors='ignore')
    else:
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
        sys_p = CREATE_PROMPT.replace(SCRIPT_FORMAT_RULE + OUTPUT_CLEAN_RULE, "") + "\n\n" + GENERAL_SCRIPT_LOGIC + "\n\n" + OUTLINE_BIO_PROMPT + "\n\n" + SCRIPT_FORMAT_RULE + OUTPUT_CLEAN_RULE
    elif wmode == "短篇创作":
        # 强制路由规则 (Task Router - Skill -1)
        analysis_keywords = ["分析", "拆解", "研究", "学习", "模仿", "结构", "看看这篇", "提取", "套路"]
        creation_keywords = ["写一个", "创作一个", "生成一个", "我要写", "新写", "帮我写", "构思"]
        revision_keywords = ["改一下", "润色", "降低ai感", "重写", "修改"]
        continue_keywords = ["继续写", "接着写", "下一章"]
        
        is_revision = any(k in uinput for k in revision_keywords)
        is_continue = any(k in uinput for k in continue_keywords)
        is_creation = any(k in uinput for k in creation_keywords)
        is_analysis = any(k in uinput for k in analysis_keywords) or (bool(dtext) and not is_creation)
        
        if is_revision:
            sys_p = "你是润色专家（Skill 6）。请根据用户的要求修改文本。"
        elif is_continue:
            sys_p = "你是续写专家（Skill 4）。请根据用户的要求继续撰写内容。"
        elif is_analysis:
            sys_p = SKILL1_PROMPT
        else:
            sys_p = SKILL0_PROMPT
    else:
        sys_p = "你是专业高效的AI创作助手。"

    if dtext:
        sys_p = f"【用户已上传待分析脚本（{len(dtext)}字）】\n\n{dtext}\n\n---\n{sys_p}"

    api_messages = [{"role": "system", "content": sys_p}]
    for m in req.messages:
        if m.get("role") in ("system", "user", "assistant"):
            if m.get("images") and len(m["images"]) > 0:
                content = []
                if m.get("content"):
                    content.append({"type": "text", "text": m["content"]})
                for img_url in m["images"]:
                    content.append({"type": "image_url", "image_url": {"url": img_url}})
                api_messages.append({"role": m["role"], "content": content})
            else:
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
            fallback_uinput = uinput
            if not fallback_uinput and req.messages and len(req.messages) > 0 and req.messages[-1].get("role") == "user":
                last_content = req.messages[-1].get("content", "")
                if isinstance(last_content, list):
                    fallback_uinput = next((p["text"] for p in last_content if p.get("type") == "text"), "")
                else:
                    fallback_uinput = str(last_content)
            smart_title = extract_smart_filename(full_response, req.messages, uinput, wmode) or fallback_uinput[:20] or "创作会话"
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
            if re.search(r'^(?:#+.*|【.*)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|角色设定|故事大纲|前十集集纲|对标拆解|Step)', stripped):
                in_body = True

        if in_body:
            if any(k in stripped for k in ["集要点:", "集要点：", "字数自算", "在1000以内", "你先审", "告诉我你的想法", "选完（或告诉我", "我立刻按同样", "写完", "感觉对吗", "埋点说明", "说明：", "接下来", "还需要", "字数约", "以上就是", "符合你的", "第六集写完", "调整后的", "修改后的", "修改说明", "三重收获", "需要我"]): break
            if stripped == "---" or stripped.startswith("--- "): break
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

class SaveFileRequest(BaseModel):
    filepath: str
    content: str

@app.post("/api/save_file")
async def save_file(req: SaveFileRequest, token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    user = get_current_user_info(token, authorization)
    username = user["username"]
    fp = os.path.join(OUTPUT_DIR, req.filepath)
    if not os.path.exists(fp):
        return {"error": "文件不存在"}
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}

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
