import os

d = r'C:\Users\Administrator\Desktop\短剧对标'

for fname in ['index.html', '创作工坊.html']:
    p = os.path.join(d, fname)
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update fetch(B + '/api/chat')
    old_chat_headers = "headers: { 'Content-Type': 'application/json' }"
    new_chat_headers = "headers: Object.assign({ 'Content-Type': 'application/json' }, getAuthHeaders())"
    if old_chat_headers in content:
        content = content.replace(old_chat_headers, new_chat_headers)

    old_chat_body = "session_id: S.cid"
    new_chat_body = "session_id: S.cid, token: getToken()"
    if old_chat_body in content:
        content = content.replace(old_chat_body, new_chat_body)

    # Update listFiles fetch
    old_list = "fetch(B + '/api/files/' + sid)"
    new_list = "fetch(B + '/api/files/' + sid + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() })"
    if old_list in content:
        content = content.replace(old_list, new_list)

    # Update preview fetch
    old_prev = "fetch(B + '/api/preview/' + path)"
    new_prev = "fetch(B + '/api/preview/' + path + '?token=' + encodeURIComponent(getToken()), { headers: getAuthHeaders() })"
    if old_prev in content:
        content = content.replace(old_prev, new_prev)

    # Update delete fetch
    old_del = "fetch(B + '/api/delete/' + path, { method: 'DELETE' })"
    new_del = "fetch(B + '/api/delete/' + path + '?token=' + encodeURIComponent(getToken()), { method: 'DELETE', headers: getAuthHeaders() })"
    if old_del in content:
        content = content.replace(old_del, new_del)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print("Auth headers and token query parameters attached to API requests!")
