# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find("var resizer = document.getElementById('resizer');")
print(text[s:s+800].encode('ascii', 'ignore').decode('ascii'))
