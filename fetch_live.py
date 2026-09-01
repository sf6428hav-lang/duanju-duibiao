# -*- coding: utf-8 -*-
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('185.213.175.66', username='root', password='@3h09m6hHvLb')
stdin, stdout, stderr = ssh.exec_command('cat /opt/duanju-duibiao/创作工坊.html')
text = stdout.read().decode('utf-8')
ssh.close()
with open('live_ui.html', 'w', encoding='utf-8') as f:
    f.write(text)
