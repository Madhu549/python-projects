import yaml
import subprocess
import shlex
import os

with open("test.yaml", "r") as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)



def write_data(file_name, user_name, zone, instance_list):
    instance_path = 'Instance_path:'
    acl_path = '\n\nACL_path:'
    details = f'''---
#Connection credentials:
ansible_user: {user_name}
ansible_ssh_private_key_file: /home/edgedevops/.ssh/ansible
ansible_python_interpreter: /usr/bin/python
mount_path: /opt/SP/{zone}/
profile_path: /opt/SP/{zone}/wm/profiles
zone_name: {zone}\n\n'''

    for i in instance_list:
        instance_path += f'''
{i} : "wm/IntegrationServer/instances/{i}"'''
        acl_path += f'''
{i} : "wm/IntegrationServer/instances/{i}/config/aclmap_sm.cnf"'''

    str = details + instance_path + acl_path
    file_name = f'/home/madhu/Desktop/test/encrypted_files/{file_name}'
    with open(file_name, 'w') as f:
        f.write(str)

for i in dict.keys():
    write_data(f"{(dict[i]['alias'])}.yaml", dict[i]['user'], i, dict[i]['instances'])

def encrypt_files(path):
    for file in os.walk(path):
        command = f'ansible-vault encrypt {file} --vault-password-file key.secret'
        result = subprocess.run(shlex.split(command))
        return f'{result} for {file}'
        
encrypt_files('/home/madhu/Desktop/test/encrypted_files/')