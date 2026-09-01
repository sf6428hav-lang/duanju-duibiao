# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
s = text.find('CREATE_PROMPT =')
print(text[s:s+1500].encode('ascii', 'ignore').decode('ascii'))
