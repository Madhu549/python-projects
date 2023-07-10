#importing required modules
import yaml, os, sys, subprocess, shlex, traceback,  
from os import path

#taking system argumet inputs
system_working_directory = sys.argv[1]
release_pipeline_number = sys.argv[2]
sprint_name = sys.argv[3]
java_home = sys.argv[4]
is_password = sys.argv[5]
env = sys.argv[6]
agent_machine = str(sys.argv[7])
drop = sys.argv[8]
drop_config_path = sys.argv[9]
master_config_path = sys.argv[10]

#paths Declaration
is_config_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/config_files/{env}/is_config.yaml'
is_other_config_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/config_files/cob1/other_config.yaml'
rollback_config_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/acl_rollback_config.yaml'
java_lib_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/wM-Dependency-Jar/'
service_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/'
log_file = f'{system_working_directory}/deploymentstatus.log'
pwd_to_create_ISUser = " "

#Print error messages
def print_error_and_exit(error_message):
    print(error_message)
    sys.stderr.write(error_message)
    sys.exit(0)

#Drop/Master/IS other yaml loading
def yaml_loader(path, error_message):
  try:
    with open(path, 'r') as f:
      config = yaml.load(f, Loader= yaml.FullLoader)
      return config
  except:
    traceback.print_exc()
    print_error_and_exit(error_message)

#Drop/Master/IS other yaml Dumper
def yaml_dumper(path, data_dict, error_message):
  try:
    with open(path, 'w') as yamlfile:
      dump_data = yaml.safe_dump(data_dict, yamlfile) 
      return dump_data
  except:
    traceback.print_exc()
    print_error_and_exit(error_message)

#checking for drop existance
def check_drop():
  if drop == 'true':
    build_config = yaml_loader(drop_config_path, 'Exception occured while loading drop config file.')
  else:
    build_config = yaml_loader(master_config_path, 'Exception occured while loading master config file.')
  return build_config

other_config_is = yaml_loader(is_other_config_path, 'Exception occured while loading Is other config file.')
is_config_dict = yaml_loader(is_config_path, 'Exception occured while loading Is config file.')

#Return null if value is None passed
def return_NA_if_null(id, values, column_name):
    if id[values][column_name] != None:
        return id[values][column_name]
    else:
        return 'null'

#checking for the existence of target server alias in the is config yaml file
def checking_target_server_alias(target_alias_name):
  try:
    for target_alias in is_config_dict[target_alias_name].keys():
      target_server_alias_name = f'{env}_{target_alias}'
      return target_server_alias_name
  except KeyError:
    print(f'{target_alias_name} is not present in {env} config file\n')
    print_error_and_exit("Please add the above mentioned target server in respective environment IS Config file\n")     

# Fetching the user name and password from the other_config_is yaml file
def framing_username_and_password(username):
  for deploy_id in other_config_is['otherConfigIS']['isuser']:
    for values in deploy_id.keys():
      if deploy_id[values]['username'] == username:
        return deploy_id[values]['username'], deploy_id[values]['password']
  else:
    return other_config_is['otherConfigIS']['isuserdefault']['username'], other_config_is['otherConfigIS']['isuserdefault']['password']

#framing of acl data as a string with a comma separated values
def framing_acl_data():
  ACL_NAME_LIST, ACL_SERVICE_LIST, ACTION_LIST, ARTIFACT_TYPE_LIST, ERROR_MESSAGE_LIST, FOR_DEPLOYMENT_LIST, GROUPNAME_LIST, ROLLBACK_ID_LIST, STATUS_LIST, target_server_list1, USERNAME_LIST, pwd_to_create_ISUser_list, target_server_list2, target_server_list = [], [], [], [], [], [], [], [], [], [], [], [], [], []
  for otherisconfig in build_config.keys():
    if otherisconfig == 'otherisconfig':
      for id in build_config[otherisconfig]:
        for values in id.keys():
          ACL_NAME_LIST.append(return_NA_if_null(id, values, 'ACL_NAME'))
          ACL_SERVICE_LIST.append(return_NA_if_null(id, values, 'ACL_SERVICE'))
          ACTION_LIST.append(return_NA_if_null(id, values, 'ACTION'))
          ARTIFACT_TYPE_LIST.append(return_NA_if_null(id, values, 'ARTIFACT_TYPE'))
          ERROR_MESSAGE_LIST.append(return_NA_if_null(id, values, 'ERROR_MESSAGE'))
          FOR_DEPLOYMENT_LIST.append(return_NA_if_null(id, values, 'FOR_DEPLOYMENT'))
          GROUPNAME_LIST.append(return_NA_if_null(id, values, 'GROUPNAME'))
          ROLLBACK_ID_LIST.append(str(return_NA_if_null(id, values, 'ROLLBACK_ID')))
          STATUS_LIST.append(return_NA_if_null(id, values, 'STATUS'))          
          try:
            target_server_list1.append(return_NA_if_null(id, values, 'TARGET_SERVER_ALIAS').split(','))
            for alias_list in target_server_list1:
              for alias in alias_list:
                target_server_list2.append(checking_target_server_alias(alias))
            target_server_list.append(':'.join(target_server_list2))
            target_server_list1.clear()
            target_server_list2.clear()
          except:
            print_error_and_exit('error occured in framing target server alias list')
          try:
            #function call for user name and password
            u_name = return_NA_if_null(id, values, 'USERNAME')           
            U_name_and_password = framing_username_and_password(u_name)
            USERNAME_LIST.append(U_name_and_password[0])
            pwd_to_create_ISUser_list.append(U_name_and_password[1])
          except:
            print_error_and_exit('error occurd in framing is user name and password')

  ACL_NAME =  ','.join(ACL_NAME_LIST)
  ACL_SERVICE = ','.join(ACL_SERVICE_LIST)
  ACTION = ','.join(ACTION_LIST)
  ARTIFACT_TYPE = ','.join(ARTIFACT_TYPE_LIST)
  ERROR_MESSAGE = ','.join(ERROR_MESSAGE_LIST)
  FOR_DEPLOYMENT = ','.join(FOR_DEPLOYMENT_LIST)
  GROUPNAME = ','.join(GROUPNAME_LIST)
  ROLLBACK_ID = ','.join(ROLLBACK_ID_LIST)
  STATUS =  ','.join(STATUS_LIST)
  target_server_alias_list = ','.join(target_server_list)
  USERNAME = ','.join(USERNAME_LIST)
  pwd_to_create_ISUser = ','.join(pwd_to_create_ISUser_list)

  return ACL_NAME, ACL_SERVICE, ACTION, ARTIFACT_TYPE, ERROR_MESSAGE, FOR_DEPLOYMENT, GROUPNAME, ROLLBACK_ID, STATUS, target_server_alias_list, USERNAME, pwd_to_create_ISUser

#preparing is config data from the is config dictonary
def framing_is_details():
  rollbackId = 0
  protocol = "http"
  is_host = is_config_dict['DeployerServer'][agent_machine]['host']
  is_port = is_config_dict['DeployerServer'][agent_machine]['port']    
  is_user_name = is_config_dict['DeployerServer'][agent_machine]['user']
  server = f'{str(is_host)}:{str(is_port)}'
  pwd_to_create_ISUser = " " 

  return rollbackId, protocol, is_user_name, server, pwd_to_create_ISUser   

#Invoking WM service to deploy the ACL data that the user wants to create, delete and Asiign
def acl_group_deployment():
  print(list(build_config.keys()))
  if 'otherisconfig' not in list(build_config.keys()):
    rollback_data = {}
    doc = yaml_dumper(rollback_config_path, rollback_data, 'Exception occured while dumping data into rollback config file.')
    rollback_config_data = yaml_loader(rollback_config_path, 'Exception occured while loading rollback config file.')
  try:
    is_details_list = framing_is_details()
    print('successfully fetched is details')
    print(is_details_list)
    for id in build_config['otherisconfig']:
      if id[list(id.keys())[0]]['FOR_DEPLOYMENT'] == 'DEPLOY':
        acl_data_list = framing_acl_data()
  except KeyError:
    print("No ACL Groups are found for this deployment")  
  except:
    traceback.print_exc()
    print_error_and_exit("Exception occured in ACL Groups python script")     
  return acl_data_list, is_details_list

#framing yaml from dictionary file in rollback_config_path
def framing_rollback_yaml(rollbackId):
  for data in build_config['otherisconfig']:
    for id in data.keys():
      if rollbackId == id:
        if not os.path.exists(rollback_config_path):
          doc = yaml_dumper(rollback_config_path, data, 'Exception occured while dumping data into rollback config file.')
          rollback_config_data = yaml_loader(rollback_config_path, 'Exception occured while loading rollback config file.')                        
        else:
          rollback_config_data = yaml_loader(rollback_config_path , 'Exception occured while loading rollback config file.')          
          rollback_config_data.update(data)
          yaml_dumper(rollback_config_path, rollback_config_data, 'Exception occured while dumping data into rollback config file.')

#Invoking WM service and sending the email notification on the result
def send_email_alert(artifact_type = "ISUserGroupACLs"): 
  if 'otherisconfig' in build_config.keys():
    try:
      deployment_action = "DEPLOY"    
      Service_to_invoke_mail = "VfDevOpsAutomationServices.service.priv:sendEMailAlert"

      #function call for preparing Is details
      rollbackId, protocol, is_user_name, server, pwd_to_create_ISUser = framing_is_details()
      java_Exec=f'{java_home}/bin/java -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar invokeService {protocol} "{server}" {is_user_name} {is_password} "{Service_to_invoke_mail}" "ReleaseName|{release_pipeline_number}" "SprintName|{sprint_name}" "LogFile|{log_file}" "Drop|{drop}" "ArtefactType|{artifact_type}" "ActionForDeployment|{deployment_action}" "Env|{env}"'

      output_mail=os.system(java_Exec)
      if(str(output_mail) or output_mail == '0'):
        print("Mail notification sent")
    except:
      traceback.print_exc()
      print_error_and_exit("Exception occured while sending mail notification")

# main function call
if __name__=='__main__':
    try:
      print('excecution of acl deployment started')
      build_config  = check_drop()
      data = acl_group_deployment()
      acl_name, acl_service, action, artifact_type, error_message, for_deployment, groupname, rollback_id, status, target_server_alias, username, pwd_to_create_ISUser, rollbackId, protocol, is_user_name, server = data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][9], data[0][10], data[1][0], data[1][1], data[1][2], data[1][3], data[1][4]
      print(acl_name, '\n\n', acl_service, '\n\n', action, '\n\n', artifact_type, '\n\n', error_message, '\n\n', for_deployment, '\n\n', groupname, '\n\n', rollback_id, '\n\n', status, '\n\n', target_server_alias, '\n\n', username, '\n\n', pwd_to_create_ISUser, '\n\n', rollbackId, '\n\n', protocol, '\n\n', is_user_name, '\n\n', server)
      
    except:
      traceback.print_exc()
      print_error_and_exit("Exception occured in ACL Group deployment script")
    
