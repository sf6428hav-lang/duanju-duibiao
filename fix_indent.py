# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'elif is_design or (is_creation and not dtext) or (wmode == "短剧对标" and any(k in uinput for k in ["仿写", "创新", "改编"])):' in lines[i]:
        # Fix indentation for the next few lines
        lines[i+1] = '            sys_p = SKILL2_PROMPT\n'
        lines[i+2] = '            try:\n'
        lines[i+3] = '                import os\n'
        lines[i+4] = '                base_dir = os.path.dirname(os.path.abspath(__file__))\n'
        lines[i+5] = '                with open(os.path.join(base_dir, "知识库_调用规则.md"), "r", encoding="utf-8") as f_r:\n'
        lines[i+6] = '                    r_txt = f_r.read()\n'
        lines[i+7] = '                with open(os.path.join(base_dir, "知识库_短篇言情爆款梗库.md"), "r", encoding="utf-8") as f_t:\n'
        lines[i+8] = '                    t_txt = f_t.read()\n'
        lines[i+9] = '                sys_p += f"\\n\\n========== 以下为系统动态挂载的本地梗库数据 ==========\\n\\n{r_txt}\\n\\n{t_txt}\\n==================================================\\n"\n'
        lines[i+10] = '            except Exception as e:\n'
        lines[i+11] = '                print("Failed to load KB:", e)\n'
        break

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Indentation fixed")
