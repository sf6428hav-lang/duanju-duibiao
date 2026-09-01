# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('function closeEditor')
with open('close_editor.txt', 'w', encoding='utf-8') as out:
    out.write(text[s:s+400])
