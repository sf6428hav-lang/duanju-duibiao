# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_scroll = 'let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 150;'
new_scroll = 'let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 20;'

text = text.replace(old_scroll, new_scroll)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("index.html fixed")
