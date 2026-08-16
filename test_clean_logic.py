import re, sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_clean_document_body(content: str, wmode: str = "") -> tuple[str, str, str]:
    if not content:
        return "", "", ""

    # 1. 彻底去除 <thinking>...</thinking>
    text = re.sub(r'<thinking>[\s\S]*?</thinking>', '', content, flags=re.IGNORECASE).strip()

    # 2. 彻底去除 [TEMPLATEJSON]...[/TEMPLATEJSON]
    text = re.sub(r'\[TEMPLATEJSON\][\s\S]*?\[/TEMPLATEJSON\]', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'```json[\s\S]*?```', '', text, flags=re.IGNORECASE).strip()

    # 3. 识别正式成果标识
    has_analysis = bool(re.search(r'(?:对标拆解|拆解分析|爆款公式拆解|Step1-3|Step5-6|对标方案)', text)) or (wmode == "短剧对标" and ("拆解" in text or "分析方案" in text))
    has_character = bool(re.search(r'(?:人物小传|角色设定|人设小传|【角色小传】|^#+\s*人物小传)', text))
    has_outline = bool(re.search(r'(?:故事大纲|剧情大纲|三幕式大纲|^#+\s*故事大纲)', text))
    has_ep_outline = bool(re.search(r'(?:前十集集纲|分集集纲|前10集集纲|^#+\s*集纲)', text))
    has_script = bool(re.search(r'(?:第一集|第1集|【第一集】|【第1集】|^#*\s*第一集|^#*\s*第1集|\b[0-9]+-[0-9]+集正文\b)', text)) or ("场次：" in text and "▲" in text)

    doc_type = ""
    label_suffix = ""

    # 优先级设定：分析报告 > 角色小传 > 故事大纲 > 集纲 > 剧本正文
    if has_analysis and len(text) >= 150:
        doc_type = "analysis"
        label_suffix = "对标拆解分析方案"
    elif has_character and len(text) >= 150:
        doc_type = "character"
        label_suffix = "人物小传与角色设定"
    elif has_outline and len(text) >= 150:
        doc_type = "outline"
        label_suffix = "故事大纲"
    elif has_ep_outline and len(text) >= 150:
        doc_type = "episode_outline"
        label_suffix = "前十集集纲"
    elif has_script and len(text) >= 150:
        doc_type = "script"
        ep_range = re.findall(r'(?:第|\b)([0-9]+-[0-9]+)(?:集|\b)', text)
        if ep_range:
            label_suffix = f"第{ep_range[0]}集剧本正文"
        else:
            label_suffix = "剧本正文"

    # 如果只是局部对话修改/微调，字数少且没有完整的结构标题，决不保存为独立文件！
    if not doc_type:
        return "", "", ""

    # 4. 清洗行：去除前后闲聊/思考草稿/对话总结
    lines = text.splitlines()
    clean_lines = []
    in_body = False

    for line in lines:
        stripped = line.strip()
        if not in_body:
            if re.search(r'^(?:#|【|第[0-9一二三四五六七八九十]+集|第一集|人物小传|角色小传|故事大纲|前十集集纲|对标拆解|拆解分析|一、|二、|三、|▲|场次：)', stripped):
                in_body = True
            elif len(stripped) > 0 and not any(k in stripped for k in ["之前那版", "用户要", "控制在", "字数：", "符合", "极简", "设计（", "好的，", "这是为您"]):
                in_body = True

        if in_body:
            if any(stripped.startswith(k) for k in ["数一下字数", "符合要求", "请确认是否", "你定一下", "请在下方说明"]):
                continue
            clean_lines.append(line)

    result = "\n".join(clean_lines).strip()
    return doc_type, result, label_suffix


# Test Case 1: 用户的截图案例 (局部闪回修改，约90字) -> 应当被过滤，不保存！
sample1 = """
<thinking>
用户要：闪回更简短，控制在100字以内，主要交代男主“被暗算”。
</thinking>

之前那版约130字，且是“诡异裂缝白光卷走”（谜团式），用户现在明确要“交代被暗算”——所以要点明是被暗算/偷袭...

设计（100字内）：
【闪回·被暗算】
▲九天之上，玄衣男子凌空而立...
【闪回结束】

数一下字数：约90字（含字卡、画面）。符合。
"""

# Test Case 2: 对标拆解分析完成 (完整分析) -> 应当保存为 《剧名》_对标拆解分析方案.docx！
sample2 = """
<thinking>
分析《花卷致富》对标模型...
</thinking>

# 《花卷致富：我的小吃店通古今》对标拆解分析方案

一、核心痛点与爽点拆解
1. 痛点：女主开店被极品刁难，收账无门，陷入绝境，无法在古代立足...
2. 爽点：古代灵兽降临，打脸极品亲戚，店铺暴富...

二、人物关系与矛盾矩阵
1. 女主苏晚：穿成外卖总监，手撕极品。
2. 男主陆沉：九天尊者，变成嘴贱公鸡。

三、剧情卡点与商业化布局
1. 第10集卡点：男主身份曝光...
2. 第30集卡点：大反派降临...
"""

# Test Case 3: 完整生成1-5集剧本正文 -> 应当保存为 《剧名》_第1-5集剧本正文.docx！
sample3 = """
<thinking>
生成第1-5集正文...
</thinking>

# 《穿成外卖女总监》第1-5集剧本正文

第一集
场次：1-1
场景：外卖店

▲女主快速打包外卖，满头大汗。
女主：快！送往九天灵山！
男主（公鸡）：放开本尊！本尊乃九天无上仙尊！
▲公鸡疯狂蹦跳，撞翻油炸锅。

第二集
场次：2-1
场景：街道
▲女主骑电动车飞驰，风驰电掣。
▲天空中雷电交加，异象突生。
"""

dt1, r1, l1 = extract_clean_document_body(sample1, "剧本创作")
print(f"Sample 1 (90字微调) -> DocType: '{dt1}', Label: '{l1}', Saved: {bool(dt1)}")

dt2, r2, l2 = extract_clean_document_body(sample2, "短剧对标")
print(f"Sample 2 (对标分析) -> DocType: '{dt2}', Label: '{l2}', Saved: {bool(dt2)}, Len: {len(r2)}")

dt3, r3, l3 = extract_clean_document_body(sample3, "剧本创作")
print(f"Sample 3 (1-5集正文) -> DocType: '{dt3}', Label: '{l3}', Saved: {bool(dt3)}, Len: {len(r3)}")
