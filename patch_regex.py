with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# We will use regex to replace the entire section of "## 🎯 一、一句话主线概括" up to "## 📊 二、题材定位"
pattern = r"## 🎯 一、一句话主线概括.*?## 📊 二、题材定位"
replacement = """## 🎯 一、一句话主线概括（爆文编辑版）
你不是总结全文，而是提炼故事最核心的矛盾。
请回答：“如果只能用一句话告诉编辑，这篇短篇讲的是什么？”

【生成规则】：
- 只保留主角关系 + 核心冲突 + 最大反转；
- 不写人物详细背景；
- 不写过程流水账；
- 不写最终结局；
- 不使用文学化表达；
- 绝不使用“觉醒、清算、身份曝光、情绪释放、满足期待”等 AI 分析词。

【推荐结构】：
> 【主角原本关系/身份】，却因为【核心矛盾】走向破裂；当【关键变化】发生后，故事迎来【核心反转】。

【强制示例】（字数控制在50-100字）：
❌ 禁止生成（带有浓烈AI模板味）：
> “她隐藏多年身份，最终完成复仇，让伤害她的人付出代价。”
✅ 允许生成（自然、有故事感、展现核心冲突）：
> “她陪丈夫创业多年，却在他成功后被抛弃。当她选择离开，丈夫才发现那个被自己忽视的女人，才是真正支撑他走到今天的人。”

## 📊 二、题材定位"""

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Replaced section via Regex.")
