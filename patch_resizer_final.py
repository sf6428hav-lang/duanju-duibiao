# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Change mainResizer to resizerRight
text = text.replace('<div class="resizer" id="mainResizer"></div>', '<div class="resizer" id="resizerRight"></div>')

# 2. Remove display:none for resizerRight in closeEditor
text = text.replace("var rr = E('resizerRight'); if(rr) rr.style.display = 'none';", "")
text = text.replace("var rr = document.getElementById('resizerRight');\n        if(rr) rr.style.display = 'block';", "")
text = text.replace("if(rr) rr.style.display = 'block';", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Patched index.html correctly!")
