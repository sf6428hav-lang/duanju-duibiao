with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith(r'\nSKILL2_PROMPT'):
        new_lines.append(line.replace(r'\nSKILL2_PROMPT', 'SKILL2_PROMPT'))
    elif line.startswith(r'\n\nSKILL3_PROMPT'):
        new_lines.append(line.replace(r'\n\nSKILL3_PROMPT', 'SKILL3_PROMPT'))
    elif line.startswith(r'\n\nSKILL4_PROMPT'):
        new_lines.append(line.replace(r'\n\nSKILL4_PROMPT', 'SKILL4_PROMPT'))
    elif line.startswith(r'\n\nSKILL6_PROMPT'):
        new_lines.append(line.replace(r'\n\nSKILL6_PROMPT', 'SKILL6_PROMPT'))
    elif r"\n\n" in line and "```" not in line and "SKILL" not in line: # generic cleanup
         # Be careful, I will just manually replace the exact string in the entire file
         pass
    
with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace(r'\nSKILL2_PROMPT', '\nSKILL2_PROMPT')
text = text.replace(r'\n\nSKILL3_PROMPT', '\n\nSKILL3_PROMPT')
text = text.replace(r'\n\nSKILL4_PROMPT', '\n\nSKILL4_PROMPT')
text = text.replace(r'\n\nSKILL6_PROMPT', '\n\nSKILL6_PROMPT')
text = text.replace(r"'\n\nBENCH_PROMPT", "'\n\nBENCH_PROMPT")
text = text.replace(r"'''\n\n", "'''\n\n")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed')
