# -*- coding: utf-8 -*-
import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'isGenerating.*?renderMarkdown\(disp\)', text, re.DOTALL)
if match:
    print(match.group(0).encode('ascii', 'ignore').decode('ascii')[-400:])
else:
    print("Not found")
