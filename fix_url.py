import os
base_dir = r'C:\Users\Administrator\Desktop\短剧对标'
files_to_fix = ['index.html', '创作工坊.html']
for fn in files_to_fix:
    path = os.path.join(base_dir, fn)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace("var B = 'http://localhost:8000';", "var B = (window.location.origin === 'file://' || window.location.origin === 'null') ? 'http://localhost:8000' : window.location.origin;")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {fn}')
