import re
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"## 🎯 一、一句话主线概括.*?## 📊 二、题材定位"
replacement = """## 🎯 一、一句话主线梳理
请用100字以内完整概括短篇故事主线。

【生成公式】：
人物关系起点 + 核心矛盾 + 主角行动 + 关键真相 + 最终结果

【要求】：
1. 必须交代故事从开始到结尾的发展方向；
2. 必须包含人物关系变化；
3. 必须包含推动剧情发展的核心冲突；
4. 必须包含最终揭露的重要真相或反转；
5. 必须保持剧情完整，但不要展开细节。

【禁止】：
❌ 写成小说简介；
❌ 只描述情绪；
❌ 只描述爽点；
❌ 使用“觉醒、逆袭、打脸、满足读者期待”等分析词；
❌ 罗列事件流水账。

【目标】：
像短篇编辑给作者快速介绍：“这篇小说到底讲了什么。”

【标准模板参考】：
> 【主角A】原本与【人物B】处于【关系/状态】，却因【核心矛盾事件】导致关系破裂。随后【主角A】采取【主要行动】，在过程中揭开【关键秘密/反转真相】，最终【人物关系或局势结果】。

## 📊 二、题材定位"""

text = re.sub(pattern, replacement, text, flags=re.DOTALL)
text = text.replace('"one_sentence_selling_point": "[一句话主线概括]"', '"one_sentence_selling_point": "[一句话主线梳理]"')

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated server.py with the final one-sentence mainline formula.")
