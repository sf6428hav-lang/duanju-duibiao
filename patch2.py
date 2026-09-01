# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('elif is_design')
e = text.find('elif is_analysis', s)
old_block = text[s:e]

new_route = '''elif is_design or (is_creation and not dtext) or (wmode == "短剧对标" and any(k in uinput for k in ["仿写", "创新", "改编"])):
        sys_p = SKILL2_PROMPT
        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, "知识库_调用规则.md"), "r", encoding="utf-8") as f_r:
                r_txt = f_r.read()
            with open(os.path.join(base_dir, "知识库_短篇言情爆款梗库.md"), "r", encoding="utf-8") as f_t:
                t_txt = f_t.read()
            sys_p += f"\\n\\n========== 以下为系统动态挂载的本地梗库数据 ==========\\n\\n{r_txt}\\n\\n{t_txt}\\n==================================================\\n"
        except Exception as e:
            print("Failed to load KB:", e)
        
        '''

text = text.replace(old_block, new_route)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Routing patched")
