import yaml
import traceback
import sys, os

#taking system arguments
drop = sys.argv[1]
sprint = sys.argv[2]
environment = sys.argv[3]
doc_name = sys.argv[4]
schema = sys.argv[5]
file_name = sys.argv[6]
column_name = sys.argv[7]
column_value = sys.argv[8]
other_config_is_details = sys.argv[9]


# drop = '10,2'
# sprint = 'R23028'
# environment = 'cob1'
# doc_name = 'VfEdgeOrderLoggingCanonical.logging:EdgeOrderTransaction'
# schema = 'edge_config, edge_process'
# file_name = '6_INSERT_ENV_PROPERTIES_CONFIG.sql, 35_INSERT_ENV_PROPERTIES_CONFIG.sql'
# column_name = 'Servername, com_data'
# column_value = '/opt/SP/edge/comdata/wmedgtsk14/SupplierFootprintData, sample_com/data/path'
# other_config_is_details = '1:EdgeFABHUBUser:EdgeFABHUBUser, 2:EdgeDevopsUser:EdgeDevopsUser, 18:EdgeDevopsUser:EdgeDevopsUser'


otherConfigDocSync_dict, otherConfigDB_dict, otherConfigIS_dict = {}, {}, {}

def get_isuserdefault_data():
  if not environment in ['cob1', 'cob2']:   
    user_name = 'situser'
    pwd = 'situser'
  user_name = 'med_llu_vodafone_user'
  pwd = 'Pa55w0rd'
  return user_name, pwd

def yaml_dumper(dict, other_config_file_path):
  try:
    with open(other_config_file_path, 'w') as f:
      yaml.dump(dict, f)
      print(f'##[INFO]: Other config file created successfully with the given data')
  except:
    print_error_and_exit('Error occured while dumping dictonary to other_config yaml file............')

#Drop/Master/IS other yaml loading
def yaml_loader(path, error_message):
  if os.path.exists(path):
    try:
      with open(path, 'r') as file:
        yaml.load(file, Loader= yaml.FullLoader)
        print('##[INFO]: The Given Yaml file is in proper Format')
    except:
      traceback.print_exc()
      print_error_and_exit(error_message)
  else:
    print_error_and_exit(f'Invalid path: {path}.............')

def print_error_and_exit(error_message):
  print(f'{error_message}............\n')
  sys.stderr.write(error_message)
  sys.exit(0)

def get_other_config_is():
  acl_default_user, acl_default_pwd = get_isuserdefault_data()
  other_config_is_details_list = other_config_is_details.split(',')
  for i in range(len(other_config_is_details_list)):
    otherConfigIS_dict.setdefault('otherConfigIS', {}).setdefault('isuser', {}).update({int(other_config_is_details_list[i].split(':')[0].strip()): {'username': other_config_is_details_list[i].split(':')[1].strip(), 'password': other_config_is_details_list[i].split(':')[1].strip()}})
    otherConfigIS_dict.setdefault('otherConfigIS', {}).setdefault('isuserdefault', {}).update({'username': acl_default_user, 'password': acl_default_pwd})
  return otherConfigIS_dict

def get_instance():
  if environment not in ['cob1', 'cob2']:
    target_alias = 'b2b_wm2,bpms_wm2,edge_wm2,edge_wm4,edgeb2b_wm3,edgeb2b_wm4,edgetask_wm2'
  target_alias = 'b2b_wm2_pr, bpms_wm2_pr, edge_wm2_pr, edge_wm4_pr, edgeb2b_wm3_pr, edgeb2b_wm4_pr, edgetask_wm2_pr, b2b_wm2_sw, bpms_wm2_sw, edge_wm2_sw, edge_wm4_sw, edgeb2b_wm3_sw, edgeb2b_wm4_sw, edgetask_wm2_sw'
  return target_alias

def get_table_data():
  instances = get_instance()
  doc_name_list = doc_name.split(',')
  table_data_list = []
  for i in range(len(doc_name_list)):
    table_data_list.extend([f'''Insert into DEPLOYMENT_DOCSYNC(RELEASE_NAME, DOC_NAME, STATUS, TARGET_SERVER_ALIAS, FAILED_SERVER_ALIAS, ACTION, UPDATED_TIMESTAMP, ENVIRONMENT, ERROR_MESSAGE) values({sprint}, {doc_name.split(',')[i].strip()}, 'NEW', {instances}, null, 'DEPLOY', 'to_timestamp(22-08-22 10:52:08.000000000 AM, DD-MM-RR HH12:MI:SSXFF AM)', {environment}, null)'''])
  table_data_list.extend(['COMMIT'])
  return table_data_list
  
def get_doc_sync():
  table_data = get_table_data()
  otherConfigDocSync_dict['otherConfigDocSync'] = {sprint: table_data}
  return otherConfigDocSync_dict

def get_other_config_db():
  schema_list = schema.split(',')
  file_name_list = file_name.split(',')
  column_name_list = column_name.split(',')
  column_value_list = column_value.split(',')
  drop_list = drop.split(',')
  for i in range(len(schema_list)):
    otherConfigDB_dict.setdefault('otherConfigDB', {}).setdefault(sprint, {}).update({int(drop_list[i].strip()): {schema_list[i].strip(): {file_name_list[i].strip(): {column_name_list[i].strip(): column_value_list[i].strip()}}}})
  return otherConfigDB_dict

def get_other_config_dict():
  other_config_is = get_other_config_is()
  doc_sync = get_doc_sync()
  other_config_db = get_other_config_db()
  return {**other_config_db, **doc_sync, **other_config_is}

def prepare_other_config_yaml():
  other_config_dict = get_other_config_dict()
  yaml_dumper(other_config_dict, 'other_config_test.yaml')

#main function call
if __name__=='__main__':
  prepare_other_config_yaml()