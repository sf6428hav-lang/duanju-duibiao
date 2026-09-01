# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<div class="main">')
if s != -1:
    print(text[s-100:s+100])
