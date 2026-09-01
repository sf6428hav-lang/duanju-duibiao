# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('onclick="rgn(')
if s != -1:
    print(text[s:s+150])
