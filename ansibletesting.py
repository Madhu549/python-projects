import sys
import os
import yaml 
import subprocess
import shlex

sys_working_dir = sys.argv[1]
env = sys.argv[2]
zones = sys.argv[3]
inventory = f'{sys_working_dir}/_webMethods-Upgrade/config_files/Old/{env}/hosts'
play_path = f'{sys_working_dir}/_webMethods-Upgrade/playbooks/fetch_property_files.yaml'

###### Fetch Urls from remote servers ######
play_command = f' ansible-playbook {play_path} --limit {zones} -i {inventory} --extra-vars "storage_path={sys_working_dir}"'

print (f'##[command] {play_command}')

result = subprocess.run(shlex.split(play_command))

print(f"Completed Playbook execution with return Result: {result.returncode}")

if result.returncode != 0:
    raise Exception(f"##[error] Playbook execution has failed with return code: {result.returncode}")

###### Converting Grep Results into Yaml Files ######

for root, dir, files in os.walk(f"{sys_working_dir}/ansible_property_backup/"):
    for file in files:
        file_path = os.path.join(root, file)
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                data = f.readlines()
                data = [i.strip() for i in data]
            '''properties = [tuple(x.strip().split('=')) for x in data]
            print(*properties)
            instance_dict = [f'{x[0]}: {x[1]}' for x in properties]'''

            name, ext = os.path.splitext(file_path)
            new_yaml_file = name+'.yaml'
            os.rename(file_path, new_yaml_file)

            with open(new_yaml_file, 'w') as f:
                yaml.dump(data, f)
