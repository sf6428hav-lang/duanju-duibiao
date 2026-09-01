# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'elif wmode == \'skill2\':\s*sys_prompt = SKILL2_PROMPT.*?(?:elif wmode|else:)', text, re.DOTALL)
if m:
    print(m.group(0).encode('ascii', 'ignore').decode('ascii'))
