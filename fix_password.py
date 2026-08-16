import os
import glob

base_dir = r'C:\Users\Administrator\Desktop\短剧对标'
html_string_to_remove = '<div style="text-align:center;margin-top:12px;font-size:12px;opacity:0.6;">默认初始账号: admin / nPB5hKpCu3NnruO1</div>'
html_replacement = '<div style="text-align:center;margin-top:12px;font-size:12px;opacity:0.6;">初始密码已在后台随机生成，请查看终端输出或配置 .env</div>'

# 1. Update HTML and update_auth scripts
for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.startswith('update_'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if html_string_to_remove in content:
                content = content.replace(html_string_to_remove, html_replacement)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Fixed HTML text in: {filepath}')

# 2. Update backend py files
backend_files = ['server.py', r'扒本\main.py', r'扒本\server.py']
python_str_to_find = 'pw_hash = hashlib.sha256("nPB5hKpCu3NnruO1".encode(\'utf-8\')).hexdigest()'
python_replacement = '''import os, string, random
        admin_pass = os.environ.get("ADMIN_PASSWORD")
        if not admin_pass:
            try:
                with open("admin_password.txt", "r") as pf:
                    admin_pass = pf.read().strip()
            except FileNotFoundError:
                admin_pass = "".join(random.choices(string.ascii_letters + string.digits, k=12))
                with open("admin_password.txt", "w") as pf:
                    pf.write(admin_pass)
                print(f"\\n{'='*50}\\n注意：已生成 admin 初始密码并保存至 admin_password.txt\\n密码是: {admin_pass}\\n{'='*50}\\n")
        pw_hash = hashlib.sha256(admin_pass.encode('utf-8')).hexdigest()'''

for bf in backend_files:
    filepath = os.path.join(base_dir, bf)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if python_str_to_find in content:
            content = content.replace(python_str_to_find, python_replacement)
            # Remove the old comment
            content = content.replace('# 默认自动置入系统管理员账号 admin，密码 admin / nPB5hKpCu3NnruO1', '# 默认自动置入系统管理员账号 admin，密码从文件或环境变量读取')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed backend password logic in: {filepath}')

# 3. Add admin_password.txt to .gitignore
gitignore_path = os.path.join(base_dir, '.gitignore')
if os.path.exists(gitignore_path):
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        gitignore_content = f.read()
    if 'admin_password.txt' not in gitignore_content:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write('\nadmin_password.txt\n')
        print('Added admin_password.txt to .gitignore')
else:
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write('admin_password.txt\n')
    print('Created .gitignore and added admin_password.txt')
