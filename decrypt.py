import sys
import os
import yaml 
import subprocess
import shlex

sys_working_dir = sys.argv[1]
env = sys.argv[2]
secret_value = sys.argv[3]
key_path = sys_working_dir + '/key.secret'

def decrypt(host_file_path):
  with open(key_path, 'w') as f:
    f.write(secret_value)
  for file in os.listdir(host_file_path):
    print (file)
    if os.path.isfile(f'{host_file_path}/{file}'):
      command = f'ansible-vault decrypt {host_file_path}/{file} --vault-password-file {key_path}'
      decrypt_result = subprocess.run(shlex.split(command))
      if decrypt_result.returncode != 0:
        sys.stderr.write(f'##[error] Failed to Decrypt host_var {file} of {env}')
        continue



host_file_path = f'{sys_working_dir}/_webMethods-Upgrade/config_files/Old/{env}/host_vars'
decrypt(host_file_path)
host_file_path = f'{sys_working_dir}/_webMethods-Upgrade/config_files/New/{env}/host_vars'
decrypt(host_file_path)
host_file_path = f'{sys_working_dir}/_webMethods-Upgrade/config_files/Upgrade/host_vars'
decrypt(host_file_path)

