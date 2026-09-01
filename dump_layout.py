# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('.doc-panel {')
if s != -1:
    print("DOC-PANEL CSS:")
    print(text[s:s+400])

s2 = text.find('main-content')
if s2 != -1:
    print("MAIN-CONTENT HTML:")
    print(text[s2-200:s2+300])

