# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
text = re.sub(
    r'\.editor-pane\s*\{\s*flex:\s*1;\s*display:\s*none;\s*/\* normally none until preview is opened \*/',
    r'.editor-pane {\n      width: 50%;\n      display: flex; /* FIXED split */',
    text
)

# 2. Add mainResizer in HTML (if not already added)
if 'id="mainResizer"' not in text:
    html_pattern = r'(<div id="editorPane" class="editor-pane">.*?</div>)\s*(<div class="main">)'
    text = re.sub(html_pattern, r'\1\n  <div class="resizer" id="mainResizer"></div>\n  \2', text, flags=re.DOTALL)

# 3. Add JS for mainResizer
js_start = text.find("let resizer = document.getElementById('resizer');")
js_end = text.find("function toggleTheme()", js_start)

if js_start != -1 and js_end != -1:
    new_js = '''let resizer = document.getElementById('resizer');
    let sidebar = document.getElementById('sidebar');
    let isDragging = false;
    
    let mainResizer = document.getElementById('mainResizer');
    let editorPane = document.getElementById('editorPane');
    let isDraggingMain = false;

    if (resizer && sidebar) {
        resizer.addEventListener('mousedown', function(e) {
          isDragging = true;
          resizer.classList.add('dragging');
          document.body.style.cursor = 'col-resize';
          document.body.style.userSelect = 'none';
        });
    }
    
    if (mainResizer && editorPane) {
        mainResizer.addEventListener('mousedown', function(e) {
          isDraggingMain = true;
          mainResizer.classList.add('dragging');
          document.body.style.cursor = 'col-resize';
          document.body.style.userSelect = 'none';
        });
    }

    document.addEventListener('mousemove', function(e) {
        if (isDragging) {
            let newWidth = e.clientX;
            if (newWidth < 150) newWidth = 150;
            if (newWidth > 400) newWidth = 400;
            sidebar.style.width = newWidth + 'px';
        }
        if (isDraggingMain) {
            let sidebarWidth = sidebar.offsetWidth;
            let resizerWidth = resizer ? resizer.offsetWidth : 0;
            let newEditorWidth = e.clientX - sidebarWidth - resizerWidth;
            if (newEditorWidth < 200) newEditorWidth = 200;
            // leave at least 300px for main
            if (window.innerWidth - e.clientX < 300) newEditorWidth = window.innerWidth - sidebarWidth - resizerWidth - 300;
            editorPane.style.width = newEditorWidth + 'px';
            editorPane.style.flex = 'none';
        }
    });

    document.addEventListener('mouseup', function(e) {
        if (isDragging) {
            isDragging = false;
            resizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
        if (isDraggingMain) {
            isDraggingMain = false;
            mainResizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
    
    '''
    text = text[:js_start] + new_js + text[js_end:]

# 4. Remove `var ep = E('editorPane'); if(ep) ep.style.display = 'none';` from closeEditor
text = text.replace("var ep = E('editorPane'); if(ep) ep.style.display = 'none';", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html")
