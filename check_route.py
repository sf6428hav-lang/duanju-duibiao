# -*- coding: utf-8 -*-
import re
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
print(re.search(r'@app\.get\("/"\)[\s\S]*?def[\s\S]*?return\s+FileResponse\([^)]+\)', text).group(0))
