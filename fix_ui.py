# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix 1: JSON Masking escaping
old_render = r'''var finalHtml = renderMarkdown(noThink.replace(/\[TEMPLATEJSON\][\s\S]*?(?:\[\/TEMPLATEJSON\]|$)/g, "").replace(/```json[\s\S]*?(?:```|$)/g, "<span style=\"font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;\">⏳ 正在生成并解析系统数据...</span>"));'''

new_render = r'''var finalHtml = renderMarkdown(noThink.replace(/\[TEMPLATEJSON\][\s\S]*?(?:\[\/TEMPLATEJSON\]|$)/g, "").replace(/```json[\s\S]*?(?:```|$)/ig, "__JSON_MASK__"));
                  finalHtml = finalHtml.replace(/__JSON_MASK__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;color:var(--primary);">⏳ 正在生成并解析系统数据...</span>');'''

text = text.replace(old_render, new_render)

# Fix 2: Auto-scroll threshold to prevent scrolling war (jitter)
old_scroll = 'let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 150;'
new_scroll = 'let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 20;'

text = text.replace(old_scroll, new_scroll)

with open('创作工坊.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("UI fixes applied")
