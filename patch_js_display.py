# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove hiding logic in closeEditor
text = text.replace("var ep = E('editorPane'); if(ep) ep.style.display = 'none';", "")

# Also, there's `var rr = E('resizerRight'); if(rr) rr.style.display = 'none';` ?
# I see a reference to `resizerRight`. Did they have a right resizer?
# The user wants it permanently fixed.
# I will make sure we do not hide mainResizer.
text = text.replace("if(ep) ep.style.display = 'flex';", "")

with open('创作工坊.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched JS display none')
