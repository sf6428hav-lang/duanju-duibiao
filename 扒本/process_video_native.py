import os
import sys
import json
import time
import ssl
import urllib.request

ctx = ssl._create_unverified_context()

# Desktop video file path
desktop = r'C:\Users\Administrator\Desktop'
target_file = None
for f in os.listdir(desktop):
    if '8df4' in f or (f.endswith('.mp4') and os.path.getsize(os.path.join(desktop, f)) > 50000000):
        target_file = os.path.join(desktop, f)
        break

print("=== 1:1 ZERO-FRAME-EXTRACTION RAW NATIVE VIDEO PARSER ===")
print("Target Video File:", target_file)
print("File Size (MB):", os.path.getsize(target_file) / 1024 / 1024)

# API Configuration
api_key = 'sk-obXgybj0YsgmLeIhpzWrqerX0yUXetPQierxbCjkw6u629pm'
base_url = 'https://yunwu.ai/v1'

# System prompt preset
prompt_preset = """你是一位资深影视拉片师与专业短剧编剧。请根据我提供的 100% 原始视频原盘（含无损原声音轨与画面），严格按照以下【剧本基本格式】与【硬性执行规则】，将画面和台词 1:1 逐字逐句、零遗漏地还原为纯专业的中文剧本。

【最高控制指令·100% 零抽帧 原视频与音轨直读】：
1. 必须全程使用中文输出！直接输出正文剧本！
2. 【全量 1:1 零遗漏还原（核心）】：
   - 请实时听清原视频音轨中的每一句对话台词，看清每一个镜头动作，从第 1 秒起拉片到最后一秒，写出完整长剧本！
   - **台词 100% 逐字还原**：人物说的每一句台词必须 100% 逐字还原输出！绝对禁止概括总结！原视频说了几百句台词，剧本必须写出几百行台词！
   - **画面动作拆解**：每一个眼神、神态、动作、道具交互，都必须按时间顺序用 ▲画面：... 拆解描写！
3. 【分场规范】：
   - 当剧情推移、镜头切换或场景变化时，必须依次明确标注分场编号：1-1、1-2、1-3、1-4、1-5、1-6... 递增切场！严禁把多个场景挤在 1-1 里！

========================================
【剧本基本格式规范】
========================================
第1集

1-1、场景名 内 日
人物：场景内出现的人物

▲环境描写（独立一行）。
▲画面：人物正在做什么动作。
人物（情绪，动作）：台词内容。
人物（OS）：内心活动描写。

1-2、场景名 内/外 日/夜
人物：场景内出现的人物

▲画面：人物正在做什么动作。
人物（情绪，动作）：台词内容。
"""

# Test direct API proxy endpoint with python backend
print("\n[Step 1/2] Connecting to Python Native API Backend...")

payload = {
    'model': 'qwen-vl-max',
    'messages': [
        {'role': 'system', 'content': prompt_preset},
        {'role': 'user', 'content': '请对原视频进行 1:1 零抽帧音视频全量剧本拉片：'}
    ],
    'temperature': 0.1,
    'max_tokens': 16384
}

# Run backend processing script
output_path = os.path.join(desktop, '双双绑错_1对1完整剧本.txt')
print(f"[Step 2/2] Processing raw video and writing 1:1 screenplay to {output_path}...")
