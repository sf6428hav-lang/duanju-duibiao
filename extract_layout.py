# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<body')
e = text.find('id="chatArea"')
if e == -1: e = s + 1000
with open('layout.txt', 'w', encoding='utf-8') as out:
    out.write(text[s:e+200])
