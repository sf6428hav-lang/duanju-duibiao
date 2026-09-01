# -*- coding: utf-8 -*-
import re
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'yield f"data: \{json\.dumps\(\{.*', text)
if match:
    s = match.start()
    print(text[max(0, s-200):s+400].encode('ascii', 'ignore').decode('ascii'))
