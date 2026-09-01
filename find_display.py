# -*- coding: utf-8 -*-
import re
with open('live_ui.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'.{0,40}display\s*=\s*[\'\"].{0,10}', text)
for m in matches:
    print(m.encode('ascii', 'ignore').decode('ascii'))
