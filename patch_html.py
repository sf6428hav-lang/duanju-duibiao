import re

def fix_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Update regex replacements to use markers
    code = code.replace(
        """                 return '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;color:var(--primary);">💾 项目资产已自动保存到系统存储</span>';""",
        """                 return '__NEED_SAVE_MARKER__';"""
    )
    code = code.replace(
        """             return '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">✨ 交互选项卡片已生成</span>';""",
        """             return '__INTERACTIVE_MARKER__';"""
    )
    code = code.replace(
        """             return '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">✨ 交互选项卡片已生成</span>';""",
        """             return '__INTERACTIVE_MARKER__';"""
    )

    # Update renderMarkdown calls in rd() and reqRd()
    old_rd_render = """        h += '<div class="content" id="msg_' + (m.id || '') + '">' + renderMarkdown(disp) + panelHtml + '</div>';"""
    new_rd_render = """        h += '<div class="content" id="msg_' + (m.id || '') + '">' + renderMarkdown(disp).replace(/__NEED_SAVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;color:var(--primary);">💾 项目资产已解析并保存到系统及项目文件</span>').replace(/__INTERACTIVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">✨ 交互选项卡片已生成</span>') + panelHtml + '</div>';"""
    code = code.replace(old_rd_render, new_rd_render)
    
    old_reqrd_render = """                  el.innerHTML = renderMarkdown(noThink.replace(/\\[TEMPLATEJSON\\][\\s\\S]*?(?:\\[\\/TEMPLATEJSON\\]|$)/g, ""));"""
    new_reqrd_render = """                  var finalHtml = renderMarkdown(noThink.replace(/\\[TEMPLATEJSON\\][\\s\\S]*?(?:\\[\\/TEMPLATEJSON\\]|$)/g, ""));
                  finalHtml = finalHtml.replace(/__NEED_SAVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;color:var(--primary);">💾 项目资产已解析并保存到系统及项目文件</span>').replace(/__INTERACTIVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">✨ 交互选项卡片已生成</span>');
                  el.innerHTML = finalHtml;"""
    code = code.replace(old_reqrd_render, new_reqrd_render)
    
    # Also fix reqRd in animation frame if it exists
    old_anim_render = """              el.innerHTML = renderMarkdown(disp);"""
    new_anim_render = """              var finalHtml = renderMarkdown(disp);
              finalHtml = finalHtml.replace(/__NEED_SAVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;color:var(--primary);">💾 项目资产已解析并保存到系统及项目文件</span>').replace(/__INTERACTIVE_MARKER__/g, '<span style="font-size:12px;opacity:.6;background:var(--bg2);padding:2px 8px;border-radius:4px;display:inline-block;margin:4px 0;">✨ 交互选项卡片已生成</span>');
              el.innerHTML = finalHtml;"""
    code = code.replace(old_anim_render, new_anim_render)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

fix_html('index.html')
try:
    fix_html('创作工坊.html')
except Exception as e:
    print(e)

print('Updated frontend HTML files')
