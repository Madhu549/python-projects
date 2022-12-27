#importing required modules
import yaml, os, sys, subprocess, shlex, traceback, pprint
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
is_other_config_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/config_files/{env}/other_config.yaml'
rollback_config_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/acl_rollback_config.yaml'
java_lib_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/wM-Dependency-Jar/'
service_path = f'{system_working_directory}/_edge-wmapps-deploy/wm_deploy_scripts/utils/'
log_file = f'{system_working_directory}/deploymentstatus.log'
pwd_to_create_ISUser = " "

#Print error messages
def print_error_and_exit(error_message):
  print(error_message)
  traceback.print_exc()
  sys.stderr.write(error_message)
  sys.exit(0)

#Drop/Master/IS other yaml loader
def yaml_loader(path, error_message):
  try:
    with open(path, 'r') as f:
      config = yaml.load(f, Loader= yaml.FullLoader)
      return config
  except:
    print_error_and_exit(error_message)

#Drop/Master/IS other yaml Dumper
def yaml_dumper(path, data_dict, error_message):
  try:
    with open(path, 'w') as yamlfile:
      dump_data = yaml.safe_dump(data_dict, yamlfile) 
      return dump_data
  except:
    print_error_and_exit(error_message)

#checking for drop existance
def check_drop():
  if drop == 'true':
    build_config = yaml_loader(drop_config_path, 'Exception occured while loading drop config file.')
  else:
    build_config = yaml_loader(master_config_path, 'Exception occured while loading master config file.')
  return build_config

#framing dictionaries for is config and other is config yaml files
other_config_is = yaml_loader(is_other_config_path, 'Exception occured while loading Is other config file.')
is_config_dict = yaml_loader(is_config_path, 'Exception occured while loading Is config file.')

#Return null if value is None passed
def return_NA_if_null(i, column_name):
  if i[column_name] != None:
    return str(i[column_name]).strip()
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
def framing_acl_data(deployment_list):
  acl_name_list, acl_service_list, action_list, artifact_type_list, error_message_list, for_deployment_list, groupname_list, rollback_id_list, status_list, target_server_list1, username_list, pwd_to_create_ISUser_list, target_server_list2, target_server_list = [], [], [], [], [], [], [], [], [], [], [], [], [], []
  for i in deployment_list:
    acl_name_list.append(return_NA_if_null(i, 'ACL_NAME'))
    acl_service_list.append(return_NA_if_null(i, 'ACL_SERVICE'))
    action_list.append(return_NA_if_null(i, 'ACTION'))
    artifact_type_list.append(return_NA_if_null(i, 'ARTIFACT_TYPE'))
    error_message_list.append(return_NA_if_null(i, 'ERROR_MESSAGE'))
    for_deployment_list.append(return_NA_if_null(i, 'FOR_DEPLOYMENT'))
    groupname_list.append(return_NA_if_null(i, 'GROUPNAME'))
    rollback_id_list.append(str(return_NA_if_null(i, 'ROLLBACK_ID')))
    status_list.append(return_NA_if_null(i, 'STATUS'))          
    try:
      target_server_list1.append(return_NA_if_null(i, 'TARGET_SERVER_ALIAS').split(','))
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
      u_name = return_NA_if_null(i, 'USERNAME')      
      U_name_and_password = framing_username_and_password(u_name)
      username_list.append(U_name_and_password[0])
      pwd_to_create_ISUser_list.append(U_name_and_password[1])
    except:
      print_error_and_exit('error occurd in framing is user name and password')

  acl_name =  ','.join(acl_name_list)
  acl_service = ','.join(acl_service_list)
  action = ','.join(action_list)
  artifact_type = ','.join(artifact_type_list)
  error_message = ','.join(error_message_list)
  for_deployment = ','.join(for_deployment_list)
  groupname = ','.join(groupname_list)
  rollback_id = ','.join(rollback_id_list)
  status =  ','.join(status_list)
  target_server_alias_list = ','.join(target_server_list)
  username = ','.join(username_list)
  pwd_to_create_ISUser = ','.join(pwd_to_create_ISUser_list)

  return acl_name, acl_service, action, artifact_type, error_message, for_deployment, groupname, rollback_id, status, target_server_alias_list, username, pwd_to_create_ISUser

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
  deployment_list = []
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
        deployment_list.append(id[list(id.keys())[0]])
    acl_data_list = framing_acl_data(deployment_list)
  except KeyError:
    print("No ACL Groups are found for this deployment")  
  except:
    print_error_and_exit("Exception occured in ACL Groups python script")     
  return acl_data_list, is_details_list

#framing yaml from dictionary file in rollback_config_path
def framing_rollback_yaml(rollback_id):
  try:
    for roll_id in rollback_id.split(','):
      for data in build_config['otherisconfig']:
        for id in data.keys():
          if roll_id == str(id):
              if not os.path.exists(rollback_config_path):
                print('path not exits')
                yaml_dumper(rollback_config_path, data, 'Exception occured while dumping data into rollback config file.')
                rollback_config_data = yaml_loader(rollback_config_path, 'Exception occured while loading rollback config file.')               
              else:
                rollback_config_data = yaml_loader(rollback_config_path , 'Exception occured while loading rollback config file.')      
                rollback_config_data.update(data)
                yaml_dumper(rollback_config_path, rollback_config_data, 'Exception occured while dumping data into rollback config file.')
  except:
    print_error_and_exit('Exception occured while framing rollback config file')
    
#fuction to caal WM service for rollback
def invoke_wm_service(acl_name, acl_service, action, artifact_type, error_message, for_deployment, groupname, status, target_server_alias, username, pwd_to_create_ISUser, protocol, is_user_name, server):
  service_to_invoke = "VfDevOpsAutomationServices.service.pub:deployUsersGroupsACLs"
  java_Compile = f'{java_home}/bin/javac -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar {service_path}invokeService.java'
  subprocess.call(shlex.split(java_Compile))
  os.chdir(service_path)
  os.system("pwd")

  java_Exec = f'{java_home}/bin/java -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar invokeService {protocol} "{server}" {is_user_name} {is_password} "{service_to_invoke}" "{acl_name}" "{acl_service}" "{action}" "{artifact_type}" "{error_message}" "{for_deployment}" "{groupname}" "{status}" "{target_server_alias}" "{username}" "SprintName|{sprint_name}" "LogFile|{log_file}" "ReleaseName|{release_pipeline_number}" "PASSWORD|{pwd_to_create_ISUser}"'

  output = os.system(java_Exec)
  return output

#Invoking WM service and sending the email notification on the result
def send_email_alert(protocol, is_user_name, server, artifact_type = "ISUserGroupACLs"): 
  if 'otherisconfig' in build_config.keys():
    deployment_action = "DEPLOY"    
    Service_to_invoke_mail = "VfDevOpsAutomationServices.service.priv:sendEMailAlert"
    java_Compile = f'{java_home}/bin/javac -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar {service_path}invokeService.java'
    subprocess.call(shlex.split(java_Compile))

    java_Exec=f'{java_home}/bin/java -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar invokeService {protocol} "{server}" {is_user_name} {is_password} "{Service_to_invoke_mail}" "ReleaseName|{release_pipeline_number}" "SprintName|{sprint_name}" "LogFile|{log_file}" "Drop|{drop}" "ArtefactType|{artifact_type}" "ActionForDeployment|{deployment_action}" "Env|{env}"'

    output = os.system(java_Exec)
    return output

# main function call
if __name__=='__main__':
    try:
      print('excecution of acl deployment started')
      build_config  = check_drop()
      data = acl_group_deployment()
      acl_name, acl_service, action, artifact_type, error_message, for_deployment, groupname, rollback_id, status, target_server_alias, username, pwd_to_create_ISUser, rollbackId, protocol, is_user_name, server = data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][9], data[0][10], data[1][0], data[1][1], data[1][2], data[1][3], data[1][4]
      print(acl_name, '\n\n', acl_service, '\n\n', action, '\n\n', artifact_type, '\n\n', error_message, '\n\n', for_deployment, '\n\n', groupname, '\n\n', rollback_id, '\n\n', status, '\n\n', target_server_alias, '\n\n', username, '\n\n', pwd_to_create_ISUser, '\n\n', rollbackId, '\n\n', protocol, '\n\n', is_user_name, '\n\n', server)
    except:
      print_error_and_exit("Exception occured in fetching ACL Group deployment data")
    
    try:
      output_wm_service = invoke_wm_service(acl_name, acl_service, action, artifact_type, error_message, for_deployment, groupname, status, target_server_alias, username, pwd_to_create_ISUser, protocol, is_user_name, server)
      if(output_wm_service or str(output_wm_service) == '0'):
        print('successfully invoked and ran WM service.')
        framing_rollback_yaml(rollback_id)
    except:
      print_error_and_exit('Exception occured while invoking and running the wm service')
    
    try:
      mail_output = send_email_alert(protocol, is_user_name, server, artifact_type)
      if(str(mail_output) or mail_output == '0'):
        print("Mail notification sent")
    except:
      print_error_and_exit("Exception occured while sending mail notification")