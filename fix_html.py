import os

def main():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "创作工坊.html")
    if not os.path.exists(html_path):
        print("找不到 创作工坊.html 文件！")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("OK")

if __name__ == "__main__":
    main()
