# -*- coding: utf-8 -*-
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = '''完成以上判断后，直接输出压缩后的：
一、一句话主线骨架
【注意】：严禁输出“出轨 → 婚礼 → 反转 → 杀人 → 复仇”这种剧情节点链！必须是高度抽象的主线骨架，以便后续叠梗创新使用。
示例：女主因丈夫背叛决裂，为查明真相展开反击，最终揭开阴谋获得自由。'''

new_str = '''完成以上判断后，必须严格按照以下模板填空，输出压缩后的：
一、一句话主线骨架
【注意】：严禁输出“出轨 → 婚礼 → 反转 → 杀人 → 复仇”这种剧情节点链！必须是高度抽象的主线骨架，以便后续叠梗创新使用。
主线模板：
【主角姓名】原本是【身份/关系】，却因【核心冲突事件】导致【人生变化】。为了【核心目标】，她/他决定【主要行动】，却遭遇【主要阻力】。最终通过【解决方式】，让【反派结局】，并获得【最终结果】。'''

if old_str in text:
    new_text = text.replace(old_str, new_str)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Successfully updated SKILL1_PROMPT')
else:
    print('String not found!')
