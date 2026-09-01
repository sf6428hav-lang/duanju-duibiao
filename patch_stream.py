with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_line = 'var finalHtml = renderMarkdown(noThink.replace(/\\[TEMPLATEJSON\\][\\s\\S]*?(?:\\[\\/TEMPLATEJSON\\]|$)/g, ""));'
new_line = 'var finalHtml = renderMarkdown(noThink.replace(/\\[TEMPLATEJSON\\][\\s\\S]*?(?:\\[\\/TEMPLATEJSON\\]|$)/g, "").replace(/```json[\\s\\S]*?(?:```|$)/g, "<span style=\\"font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;\\">✨ 正在生成并解析系统数据...</span>"));'

if old_line in text:
    text = text.replace(old_line, new_line)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched index.html stream rendering")
else:
    print("Could not find old_line in index.html")
