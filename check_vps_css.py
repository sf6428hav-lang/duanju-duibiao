# -*- coding: utf-8 -*-
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('185.213.175.66', username='root', password='@3h09m6hHvLb')
stdin, stdout, stderr = ssh.exec_command('cd /opt/duanju-duibiao && git log -n 1 && grep -A 5 ".editor-pane {" 创作工坊.html')
print('OUT:', stdout.read().decode('utf-8'))
ssh.close()
