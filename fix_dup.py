# -*- coding: utf-8 -*-
import re
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(r'(<div class="resizer" id="mainResizer"></div>\s*)+', r'<div class="resizer" id="mainResizer"></div>\n  ', text)
with open('创作工坊.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed duplicate resizer')
