import re

def update_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # We can just replace the whole 'if (S.mode === "短篇创作") {' block.
    # It starts around: "} else if (S.mode === '短篇创作') {" and ends at "} else if (S.mode === '剧本创作' || !S.mode || S.mode === '通用') {"
    
    start_str = "} else if (S.mode === '短篇创作') {"
    end_str = "} else if (S.mode === '剧本创作' || !S.mode || S.mode === '通用') {"
    
    start_idx = code.find(start_str)
    end_idx = code.find(end_str, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        new_block = '''} else if (S.mode === '短篇创作') {
          h += '<div class="guide-msg"><div class="guide-title">🚀 短篇生产工作流 (V6)</div><p>按照 V6 规范，请根据当前项目资产选择下一步操作：</p>';
          h += '<div class="preset-btns" style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">';
          if (S.docInfos && S.docInfos.length > 0) {
             h += '<span class="preset-btn" onclick="E(\\'chatInput\\').value=\\'深度拆解爆文结构\\';E(\\'sendBtn\\').click();">📖 深度拆解 (Skill 1)</span>';
          }
          if (S.sd && Object.keys(S.sd).length > 0) {
             h += '<span class="preset-btn" onclick="E(\\'chatInput\\').value=\\'设计全新故事大纲\\';E(\\'sendBtn\\').click();">🎨 设计大纲 (Skill 2)</span>';
             h += '<span class="preset-btn" onclick="E(\\'chatInput\\').value=\\'规划章节细纲\\';E(\\'sendBtn\\').click();">📜 规划章节 (Skill 3)</span>';
             h += '<span class="preset-btn" onclick="E(\\'chatInput\\').value=\\'撰写正文\\';E(\\'sendBtn\\').click();">✍️ 撰写正文 (Skill 4)</span>';
             h += '<span class="preset-btn" onclick="E(\\'chatInput\\').value=\\'请对上一段文本进行润色修改\\';E(\\'sendBtn\\').click();">✨ 润色修改 (Skill 6)</span>';
          }
          if (!(S.docInfos && S.docInfos.length > 0) && (!S.sd || Object.keys(S.sd).length === 0)) {
              h += '<span style="font-size:12px;opacity:.7;">请在左侧上传对标爆文，或在下方直接输入创作需求。</span>';
          }
          h += '</div></div>';
        '''
        code = code[:start_idx] + new_block + code[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

update_html('index.html')
try:
    update_html('创作工坊.html')
except:
    pass
print('Updated UI successfully')
