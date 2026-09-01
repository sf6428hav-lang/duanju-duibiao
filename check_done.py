# -*- coding: utf-8 -*-
import re
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'yield f"data: \{json\.dumps\(\{.*?done.*', text)
if match:
    print(match.group(0).encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
