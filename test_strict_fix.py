import re, sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_strict_document_body(content: str, wmode: str = "") -> tuple[str, str, str]:
    if not content:
        return "", "", ""

    # 1. 彻底去除 <thinking>...</thinking> (使用 re.DOTALL 处理跨多行)
    text = re.sub(r'<thinking>[\s\S]*?(?:</thinking>|$)', '', content, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', text, flags=re.DOTALL | re.IGNORECASE).strip()

    # 2. 彻底去除 [TEMPLATEJSON]...[/TEMPLATEJSON] 和 ```json 块
    text = re.sub(r'\[TEMPLATEJSON\][\s\S]*?(?:\[/TEMPLATEJSON\]|$)', '', text, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'```json[\s\S]*?```', '', text, flags=re.DOTALL | re.IGNORECASE).strip()

    # 3. 严格识别正式资产头部（只有含有明确的“资产级”结构标题，才算正式文档资产）
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

    # 如果没有匹配到明确的资产头部，说明这是聊天对话（备选台词、意见沟通、解说答复等），绝不存为文件！
    if not doc_type:
        return "", "", ""

    # 4. 提取纯净正文：严格从资产头部开始提取！
    lines = text.splitlines()
    clean_lines = []
    in_body = False

    for line in lines:
        stripped = line.strip()
        if not in_body:
            # 只有遇到正式标题，才开启正文收集！
            if re.search(r'^(?:#+|【)?(?:第[一二三四五六七八九十0-9]+集|第一集|第1集|人物小传|角色小传|故事大纲|前十集集纲|对标拆解分析方案|Step1-3|Step5-6)', stripped):
                in_body = True

        if in_body:
            if any(stripped.startswith(k) for k in ["数一下字数", "符合要求", "请确认是否", "你定一下", "请在下方说明"]):
                continue
            clean_lines.append(line)

    result = "\n".join(clean_lines).strip()
    if len(result) < 150:
        return "", "", ""

    return doc_type, result, label_suffix


# 测试最新截图中的备选台词对话 (用户说"再来一批台词"，AI给出 E, F, G, H, I, J, K 备选)
sample_chat_options = """
行，再来一批，风味尽量拉开，你挑顺眼的⚡ (核心都锁定"察觉灵力在恢复但不明所以+决定继续送探究竟")

带河南味的:
E. 裴无咎os: 咦，恁说怪不怪，越飞，本尊这劲儿回来得越足......中，先接着送，探探这里头啥门道。

冷峻悬疑的:
F. 裴无咎（眯眼）os: 一趟趟飞下来，散掉的修为竟在回拢......这背后，怕是没那么简单。

急于回身体的:
G. 裴无咎os: 好，好得很。灵力肯回，本尊迟早能查明是谁把本尊变成这鬼样，再回原身，跟他算账。

极短干脆的:
H. 裴无咎os: 越飞越有劲......有门道。飞。

哭笑不得自嘲的:
I. 裴无咎（叹气）os: 修了几千年，末了靠给人送饭回血。可这血......它真在回啊。忍。

反差反转的（先嫌弃后真香）:
J. 裴无咎os: 送饭？呸，跌份。可这一趟趟飞的，灵力偏偏往回长......真香。

带期待感钩子的:
K. 裴无咎os: 邪门。飞得越勤，灵力回得越明显。照这么下去......本尊倒要看看，这具鸡身子里，还藏着多少本尊不知道的事。
"""

dt, body, label = extract_strict_document_body(sample_chat_options, "剧本创作")
print(f"Chat Options Test -> DocType: '{dt}', Body Length: {len(body)}, Is Saved: {bool(dt)}")
