import traceback
import sys, os, yaml
from pprint import pprint

env = 'cob2'
#Print error messages
def print_error_and_exit(error_message):
    print(error_message)
    sys.stderr.write(error_message)
    sys.exit(0)

#Drop/Master/IS other yaml loading
def yaml_loader(path, error_message):
  try:
    with open(path, 'r') as file:
      config = yaml.load(file, Loader= yaml.FullLoader)
      return config
  except:
    traceback.print_exc()
    print_error_and_exit(error_message)

#Drop/Master/IS other yaml Demper
def yaml_dumper(path, data_dict, error_message): 
  try:
    with open(path, 'w') as yamlfile:
      dump_data = yaml.safe_dump(data_dict, yamlfile) 
      return dump_data
  except:
    traceback.print_exc()
    print_error_and_exit(error_message)

#other_config_is = yaml_loader('C:\\Users\MADHU\Desktop\\other_config_is.yaml', 'exception occured while loadin data')

def framing_username_and_password(username):
  for id in other_config_is['otherConfigIS']['isuser']:
    print(id)
    for values in id.keys():
      print(values)
      if id[values]['username'] == username:
        return id[values]['username'], id[values]['password']
  else:
    return other_config_is['otherConfigIS']['isuserdefault']['username'], other_config_is['otherConfigIS']['isuserdefault']['password']

import yaml
#checking for the existence of target server alias in the is config yaml file
def checking_target_server_alias(target_alias_name):
  try:
    for target_alias in is_config_dict[target_alias_name].keys():
      target_server_alias_name = f'{env}_{target_alias}'
      return target_server_alias_name
  except KeyError:
    print(f'{target_alias_name} is not present in {env} config file\n')
    print_error_and_exit("Please add the above mentioned target server in respective environment IS Config file\n")  

list = ['edge_wm4,edge_wm3,edge_wm2']
list1 = list[0].split(',')
list2 = []
#alias = ''
list3 = []

id_list = []
deployment_list = []

rollback_config_path = 'C:\\Users\MADHU\Desktop\\rollback_config.yaml'

data = {80 :{'ACL_NAME': 'KenanManagementV1', 'ACL_SERVICE': None, 'ACTION': 'Create', 'ARTIFACT_TYPE': 'ISUser', 'ERROR_MESSAGE': None, 'FOR_DEPLOYMENT': 'DEPLOY', 'GROUPNAME': 'KenanManagementV1', 'ROLLBACK_ID': 88, 'STATUS': 'enable', 'TARGET_SERVER_ALIAS': 'b2b_wm2', 'USERNAME': 'TestUser'}}


if not os.path.exists(rollback_config_path):
  print('path not exits')
  yaml_dumper(rollback_config_path, data, 'Exception occured while dumping data into rollback config file.')
  rollback_config_data = yaml_loader(rollback_config_path, 'Exception occured while loading rollback config file.')               
else:
  rollback_config_data = yaml_loader(rollback_config_path , 'Exception occured while loading rollback config file.')
  # pprint(data)
  # print(rollback_config_data)
  rollback_config_data.update(data)
  yaml_dumper(rollback_config_path, rollback_config_data, 'Exception occured while dumping data into rollback config file.')
rollback_list =[]
#Deleting the rollback config file after rollbacking the data successfully
def delete_temp_files(path):
  if os.path.exists(path):
    os.remove(path)
    print(f'{path} has been deleted')
  else:
    print(f'No rollback file found in this directory{path}')
    
try:
  os.chdir(rollback_config_path)
  print(os.system('pwd'))
  delete_temp_files(rollback_config_path)
except:
  print_error_and_exit('failed to delete rollback yaml file......')




#build_config = yaml_loader('C:\\Users\MADHU\Desktop\\build_config.yaml', 'exception')

#test = yaml_loader('C:\\Users\MADHU\Desktop\\other_config.yaml', 'exception')
#build_config = yaml_loader('C:\\Users\MADHU\Desktop\\master_config.yaml', 'exception')

IsConfigDict = {}
try:
    with open('master_config.yaml','r') as f:
        IsConfigDict = yaml.safe_load(f)
    
except:
    traceback.print_exc()
    sys.stderr.write("Could Not Open IS Config File\n")
#build = yaml_loader(path, 'jhdhdb')
#pprint(build_config)
#print(test)
#pprint(build_config)

drop_dict = {}
#pprint(test1)

pprint(IsConfigDict)
