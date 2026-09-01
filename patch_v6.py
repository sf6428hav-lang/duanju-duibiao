import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update SKILL1_PROMPT word limit and strict markdown ban
old_instruction = '''不要写读后感，不要写营销分析词（如：爆文发动机、情绪映射、创作建议），不要使用诸如“满足读者期待”、“极致爽感”这类主观评价。
请直接按照以下结构输出，不要使用 ** 或 - 等乱七八糟的Markdown符号，保持纯文本排版清爽，结构层次分明。'''

new_instruction = '''不要写读后感，不要写营销分析词（如：爆文发动机、情绪映射、创作建议），不要使用诸如“满足读者期待”、“极致爽感”这类主观评价。
【格式红线】：严禁在任何地方使用 **、-、# 等任何 Markdown 排版符号！必须输出绝对的纯文本格式，段落之间用换行隔开，保持排版清爽。'''

text = text.replace(old_instruction, new_instruction)

old_limit = '''[请用100-150字总结故事完整主线。必须包含：主角身份 + 核心遭遇 + 主角目标 + 主要阻力 + 解决过程 + 最终结局。不要写文学化简介，不要写营销词，不要评价作品。]'''
new_limit = '''[请用200字左右总结故事完整主线。必须包含：主角身份 + 核心遭遇 + 主角目标 + 主要阻力 + 解决过程 + 最终结局。不要写文学化简介，不要写营销词，不要评价作品。]'''

text = text.replace(old_limit, new_limit)

# 2. Update has_analysis regex to catch the new header "一、标题与一句话主线"
old_regex = r"has_analysis = bool(re.search(r'^(?:#+.*|【.*)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告|短篇爆文商业拆解报告|短篇爆文拆解报告|短篇拆解结果)', text, re.MULTILINE))"
new_regex = r"has_analysis = bool(re.search(r'^(?:#+.*|【.*)?(?:对标拆解分析方案|Step1-3拆解分析|Step5-6方案大纲|对标拆解报告|短篇爆文商业拆解报告|短篇爆文拆解报告|短篇拆解结果|一、标题与一句话主线)', text, re.MULTILINE))"
text = text.replace(old_regex, new_regex)

# 3. Add explicit markdown stripping logic before saving the document
# We find:
# cleaned_body = "\n".join(clean_lines).strip()
# if len(cleaned_body) < 150:

old_clean = '''    cleaned_body = "\\n".join(clean_lines).strip()
    if len(cleaned_body) < 150:'''

new_clean = '''    cleaned_body = "\\n".join(clean_lines).strip()
    # 强制物理清除所有残余的 Markdown 符号
    cleaned_body = re.sub(r'\\*\\*(.*?)\\*\\*', r'\\1', cleaned_body)
    cleaned_body = re.sub(r'^#+\s*', '', cleaned_body, flags=re.MULTILINE)
    cleaned_body = re.sub(r'^\s*-\s+', '', cleaned_body, flags=re.MULTILINE)
    
    if len(cleaned_body) < 150:'''
    
text = text.replace(old_clean, new_clean)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched server.py successfully")
