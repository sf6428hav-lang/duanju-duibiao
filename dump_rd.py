# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('for (var i = 0; i < msgs.length; i++) {')
e = text.find('if (S.multiSelectMode)', s)
with open('rd_loop.txt', 'w', encoding='utf-8') as out:
    out.write(text[s:e])
