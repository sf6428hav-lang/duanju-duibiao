# -*- coding: utf-8 -*-
import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<div class="sidebar" id="sidebar">.*?<div class="main">', text, re.DOTALL)
if match:
    print(match.group(0).encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
