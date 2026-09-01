with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('temp_prompts.py', 'r', encoding='utf-8-sig') as f:
    prompts = f.read()

for i, line in enumerate(lines):
    if 'BENCH_PROMPT =' in line:
        lines.insert(i, prompts + '\n\n')
        break

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
