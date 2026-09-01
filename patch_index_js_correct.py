# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

js_start = text.find("const resizer = document.getElementById('resizer');")
js_end = text.find("function toggleTheme()", js_start)

if js_start != -1 and js_end != -1:
    new_js = '''const resizer = document.getElementById('resizer');
    const sidebar = document.getElementById('sidebar');
    let isDragging = false;
    
    const mainResizer = document.getElementById('mainResizer');
    const editorPane = document.getElementById('editorPane');
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
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched index.html correctly!")
else:
    print("Could not find start or end!")
