# -*- coding: utf-8 -*-

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix SKILL1_PROMPT
text = text.replace('''"questions": [
    "A. 爆款复刻拆解（提取爽点、冲突、节奏、付费点）",
    "B. 剧情结构拆解（提取人物关系、主线、反转）",
    "C. 创作参考拆解（提取可迁移写法）"
  ]''', '''"questions": [
    {
      "question": "请选择拆解方向：",
      "options": [
        "A. 爆款复刻拆解",
        "B. 剧情结构拆解",
        "C. 创作参考拆解"
      ]
    }
  ]''')

# Fix SKILL2_PROMPT
text = text.replace('''"questions": ["A：方案一", "B：方案二", "C：方案三"]''', '''"questions": [
    {
      "question": "请选择想发展的方向：",
      "options": ["A：方案一", "B：方案二", "C：方案三"]
    }
  ]''')

# Fix routing logic in /api/chat
routing_fix = '''uinput = req.user_input or req.userinput or ""
    
    if not uinput and req.messages:
        for m in reversed(req.messages):
            if m.get("role") == "user":
                uinput = m.get("content", "")
                break
'''

text = text.replace('uinput = req.user_input or req.userinput or ""', routing_fix)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed server.py")
