# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
s = text.find("with open(history_file, 'w', encoding='utf-8') as f:")
print(text[s:s+800].encode('ascii', 'ignore').decode('ascii'))
