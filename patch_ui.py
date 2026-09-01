# -*- coding: utf-8 -*-
with open('创作工坊.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS for editor-pane
old_css = '''.editor-pane {
      flex: 1;
      display: none; /* normally none until preview is opened */
      flex-direction: column;
      background: var(--bg);
      border-right: 1px solid var(--border);
    }'''
new_css = '''.editor-pane {
      width: 50%;
      display: flex; /* FIXED split */
      flex-direction: column;
      background: var(--bg);
      border-right: 1px solid var(--border);
    }'''
if old_css in text:
    text = text.replace(old_css, new_css)
else:
    print("Could not find editor-pane css!")

# 2. Add mainResizer in HTML
old_html = '''    </div>
  </div>

  <div class="main">'''
new_html = '''    </div>
  </div>

  <div class="resizer" id="mainResizer"></div>

  <div class="main">'''
if old_html in text:
    text = text.replace(old_html, new_html)
else:
    print("Could not find main html!")

# 3. Add JS for mainResizer
old_js = '''let resizer = document.getElementById('resizer');
    let sidebar = document.getElementById('sidebar');
    let isDragging = false;

    if (resizer && sidebar) {
        resizer.addEventListener('mousedown', function(e) {
          isDragging = true;
          resizer.classList.add('dragging');
          document.body.style.cursor = 'col-resize';
          document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', function(e) {
          if (!isDragging) return;
          let newWidth = e.clientX;
          if (newWidth < 200) newWidth = 200;
          if (newWidth > 400) newWidth = 400;
          sidebar.style.width = newWidth + 'px';
        });

        document.addEventListener('mouseup', function(e) {
          if (isDragging) {
            isDragging = false;
            resizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
          }
        });
    }'''
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
    });'''
if old_js in text:
    text = text.replace(old_js, new_js)
else:
    print("Could not find js!")

with open('创作工坊.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated UI")
