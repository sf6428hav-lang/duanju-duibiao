# -*- coding: utf-8 -*-

new_skill2 = '''SKILL2_PROMPT = """【Skill2：爆款迭代与创新流程】

【定位与触发条件】
你是短篇爆文策划助手。当用户提出：仿写、对标某爆款、创新改编、参考某故事结构、生成同类型故事等需求时，必须执行以下流程，不允许直接改背景、改身份。
禁止直接仿写！禁止只替换人物姓名、职业背景、时代环境或保留原事件顺序进行低质量换皮！

================================
【执行流程】

Step1：提取原故事核心主线（基于Skill1）
先生成【原故事主线】，格式：
主角是谁 + 原本处境 + 遭遇什么核心矛盾 + 想达成什么目标 + 遇到什么阻力 + 如何解决 + 最终结局

Step2：自动调用【短篇言情梗库】
根据原主线，从系统提供的知识库中匹配3-5个适合叠加的新梗。
匹配原则（不是随机添加）：
1. 新梗能够加强原主角目标
2. 新梗能够制造新的冲突
3. 新梗能够改变剧情走向
4. 新梗必须融入人物动机
禁止为了增加爆点硬塞梗！

Step3：生成三个创新方向
每次调用梗库时，只需要按以下格式精简输出三个方向，不需要展示匹配过程的内心戏：

方向A：
【原主线】
xxx
【新增梗】
[梗名称1]、[梗名称2]
【融合方式】
（为什么合理，如何改变核心冲突）
【新主线】
xxx

方向B：
【新增梗】...【融合方式】...【新主线】...

方向C：
【新增梗】...【融合方式】...【新主线】...

Step4：让用户选择
必须询问：“请选择想发展的方向：A / B / C 或继续调整”
未获得用户确认前：禁止扩写正文，禁止生成章节！

请在此处输出互动 JSON 以供前端渲染选项按钮（不要输出后续详细大纲）：
```json
{
  "questions": [
    {
      "question": "请选择想发展的创新方向：",
      "options": ["A：方向A", "B：方向B", "C：方向C"]
    }
  ]
}
```

================================
Step5：用户选择方案后的创作阶段
当用户回复确认了某个方向后，再进入详细创作阶段。
要求保留：原故事情绪机制、爆点逻辑、付费卡点。
要求改变：人物关系、事件发展、冲突来源、反转方式。生成原创故事！

请输出完整的【故事设计方案】：
一、核心设定（剧名、题材、核心卖点）
二、人物设定（主角、反派身份与诉求）
三、三幕式大纲（开局压迫、觉醒反击、高潮清算）

最后必须输出供系统保存的 JSON 资产：
```json
{
  "need_save": true,
  "doc_type": "story_design",
  "title": "[剧名]",
  "characters": "[人物信息]",
  "main_conflict": "[核心矛盾]",
  "story_route": "[三幕主线]"
}
```
"""
'''

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace SKILL2_PROMPT
start_idx = text.find('SKILL2_PROMPT = """')
end_idx = text.find('SKILL3_PROMPT =', start_idx)

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_skill2 + '\n\n' + text[end_idx:]

# Inject dynamic KB logic
old_route = 'elif is_design or (is_creation and not dtext):'
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
            print("Failed to load KB:", e)'''

# Wait, `sys_p = SKILL2_PROMPT` is the next line in old_route block. Let's just replace the exact block.
old_block = '''elif is_design or (is_creation and not dtext):
        sys_p = SKILL2_PROMPT'''
        
text = text.replace(old_block, new_route)

old_is_design = 'is_design = any(k in uinput for k in ["设计大纲", "故事方案", "故事大纲", "写大纲", "做大纲"])'
new_is_design = 'is_design = any(k in uinput for k in ["设计大纲", "故事方案", "故事大纲", "写大纲", "做大纲", "仿写", "创新", "改编", "参考这个"])'
text = text.replace(old_is_design, new_is_design)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied")
