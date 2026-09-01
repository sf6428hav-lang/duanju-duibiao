with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = "if (!isRegen && (fullTxt || pendingImages.length > 0)) {"
new_logic = """if (isRegen) {
      if (chat.msgs.length > 0 && chat.msgs[chat.msgs.length - 1].role === 'assistant') {
          chat.msgs.pop();
      }
    }
    if (!isRegen && (fullTxt || pendingImages.length > 0)) {"""

text = text.replace(old_logic, new_logic)

with open('创作工坊.html', 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Patched 创作工坊.html regenerate bug")
