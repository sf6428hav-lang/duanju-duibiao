# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_text = text.replace('梗库需要的是“这个故事的核心矛盾是什么”', '后续改编需要的是“这个故事的核心矛盾是什么”')

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(new_text)
print('Cleaned SKILL1_PROMPT')
