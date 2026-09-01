# -*- coding: utf-8 -*-
import os

# 1. Patch server.py to enforce <think> tag globally
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# find `api_messages = [{"role": "system", "content": sys_p}]`
target = 'api_messages = [{"role": "system", "content": sys_p}]'
THINK_RULE = '\\n\\n【强制规则】：为了呈现清晰的决策过程，你必须在回答的最开始，将内部的分析、推理、以及选梗等一切决策过程，全部用 <think> 和 </think> 标签包裹起来。在 </think> 闭合标签之后，再输出给用户的正式回复和卡片内容。'
replacement = f'sys_p += "{THINK_RULE}"\n\n    {target}'

if target in text and '【强制规则】' not in text:
    text = text.replace(target, replacement)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched server.py successfully!")
else:
    print("Could not patch server.py or already patched.")

# 2. Patch index.html to fix jitter (throttle scroll to bottom)
with open('index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

scroll_target = '''let isAtB2 = E("chatArea").scrollHeight - E("chatArea").scrollTop <= E("chatArea").clientHeight + 20;
                  if(isAtB2) E("chatArea").scrollTop = E("chatArea").scrollHeight;'''

scroll_replacement = '''let ca = E("chatArea");
                  let isAtB2 = ca.scrollHeight - ca.scrollTop <= ca.clientHeight + 80;
                  if(isAtB2) {
                      if (!window._scrollT) {
                          window._scrollT = setTimeout(function() {
                              ca.scrollTop = ca.scrollHeight;
                              window._scrollT = null;
                          }, 50);
                      }
                  }'''

if scroll_target in html_text:
    html_text = html_text.replace(scroll_target, scroll_replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_text)
    print("Patched index.html jitter fix successfully!")
else:
    print("Could not patch index.html jitter fix.")
    
# also patch 创作工坊.html
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    html_text2 = f.read()
if scroll_target in html_text2:
    html_text2 = html_text2.replace(scroll_target, scroll_replacement)
    with open('创作工坊.html', 'w', encoding='utf-8') as f:
        f.write(html_text2)
    print("Patched 创作工坊.html jitter fix successfully!")
