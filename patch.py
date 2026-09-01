import re

with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update extract_smart_filename signature
code = code.replace(
    'def extract_smart_filename(content: str, messages: list = None, user_input: str = "", wmode: str = "") -> str:',
    'def extract_smart_filename(content: str, messages: list = None, user_input: str = "", wmode: str = "", doc_text: str = "") -> str:'
)

# Insert Strategy 6
strat5 = '''    # Strategy 5: Fallback to history
    if not drama_title and messages:
        for m in reversed(messages):
            mc = m.get("content", "") if isinstance(m, dict) else str(m)
            tm = re.findall(r'《([^》]+)》', mc)
            if tm:
                drama_title = tm[-1]
                break'''

strat6 = '''
    # Strategy 6: Fallback to uploaded filename from doc_text
    if not drama_title and doc_text:
        doc_match = re.search(r'【文件\d+:\s*([^】]+)】', doc_text)
        if doc_match:
            fname = doc_match.group(1).strip()
            if '.' in fname:
                fname = fname.rsplit('.', 1)[0]
            drama_title = fname'''

code = code.replace(strat5, strat5 + '\n' + strat6)

# Update process_document_saving signature
code = code.replace(
    'def process_document_saving(content: str, session_dir: str, messages: list = None, user_input: str = "", wmode: str = "") -> Optional[str]:',
    'def process_document_saving(content: str, session_dir: str, messages: list = None, user_input: str = "", wmode: str = "", doc_text: str = "") -> Optional[str]:'
)

# Update has_analysis regex
old_regex = r"has_analysis = bool(re.search(r'^(?:#+.*|【.*)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告)', text, re.MULTILINE))"
new_regex = r"has_analysis = bool(re.search(r'^(?:#+.*|【.*)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告|短篇爆文商业拆解报告|短篇爆文拆解报告|短篇拆解结果)', text, re.MULTILINE))"
code = code.replace(old_regex, new_regex)

# Update doc_type == 'analysis' label_suffix
code = code.replace(
    '        doc_type = "analysis"\n        label_suffix = "对标拆解分析方案"',
    '        doc_type = "analysis"\n        label_suffix = "分析报告"'
)

# Update in_body regex
old_in_body = r"if re.search(r'^(?:#+.*|【.*)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|角色设定|故事大纲|前十集集纲|对标拆解|Step)', stripped):"
new_in_body = r"if re.search(r'^(?:#+.*|【.*)?(?:第[0-9一二三四五六七八九十]+集|第一集|第1集|人物小传|角色小传|角色设定|故事大纲|前十集集纲|对标拆解|短篇|Step)', stripped):"
code = code.replace(old_in_body, new_in_body)

# Update final filename logic
old_filename_logic = '''    drama_title = extract_smart_filename(content, messages, user_input, wmode)
    if drama_title and label_suffix:
        final_filename = f"{drama_title}_{label_suffix}"
    elif drama_title:
        final_filename = f"{drama_title}_{label_suffix or '创作文档'}"
    else:
        final_filename = f"短剧_{label_suffix or '创作文档'}"'''

new_filename_logic = '''    drama_title = extract_smart_filename(content, messages, user_input, wmode, doc_text)
    
    if doc_type == "analysis":
        if drama_title:
            final_filename = f"分析_{drama_title}_{label_suffix}"
        else:
            final_filename = f"分析_{label_suffix}"
    else:
        if drama_title and label_suffix:
            final_filename = f"{drama_title}_{label_suffix}"
        elif drama_title:
            final_filename = f"{drama_title}_{label_suffix or '创作文档'}"
        else:
            final_filename = f"短剧_{label_suffix or '创作文档'}"'''
            
code = code.replace(old_filename_logic, new_filename_logic)

# Update call in generate()
code = code.replace(
    'saved = process_document_saving(full_response, session_dir, req.messages, uinput, wmode)',
    'saved = process_document_saving(full_response, session_dir, req.messages, uinput, wmode, req.doc_text)'
)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated server.py')
