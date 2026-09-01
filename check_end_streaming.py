# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('bench_data = extract_template_json(full_response)')
print(text[s-100:s+800].encode('ascii', 'ignore').decode('ascii'))
