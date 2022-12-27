import yaml
import os 
import subprocess
import shlex
import sys
from os import path

env = sys.argv[6]
drop_config_path= sys.argv[9]
master_config_path= sys.argv[10]
#drop_config_path= (sys.argv[1]+'/_edge-wmapps/Drop_Deployment_Configuration/drop_config.yaml')
#master_config_path= (sys.argv[1]+'/_edge-wmapps/Master_Deployment_Configuration/master_config.yaml')
config_path=(sys.argv[1]+"/_edge-wmapps-deploy/wm_deploy_scripts/config_files/"+ env +'/is_config.yaml')
is_other_config_path=(sys.argv[1]+"/_edge-wmapps-deploy/wm_deploy_scripts/config_files/"+ env +'/other_config.yaml')
java_lib_path=(sys.argv[1]+"/_edge-wmapps-deploy/wm_deploy_scripts/utils/wM-Dependency-Jar/")
releasePipelineNumber=sys.argv[2]
SprintName=sys.argv[3]
#drop_config_path= (sys.argv[1]+'/_edge-wmapps-deploy/wm_deploy_scripts/deployment_configuration/'+SprintName+'/drop_config.yaml')
#master_config_path= (sys.argv[1]+'/_edge-wmapps-deploy/wm_deploy_scripts/deployment_configuration/'+SprintName+'/master_config.yaml')
java_home=sys.argv[4]
ISPassword=sys.argv[5]
agent_machine = str(sys.argv[7])
drop= sys.argv[8]
pwd_to_create_ISUser = " "
log_file_name = 'deploymentstatus.log'
log_file = sys.argv[1]+"/"+log_file_name
rollback_config_path = (sys.argv[1]+'/_edge-wmapps-deploy/wm_deploy_scripts/utils/acl_rollback_config.yaml')

try:
  if drop == 'true':
    with open(drop_config_path) as f:
      build_config = yaml.load(f, Loader=yaml.FullLoader)
  else:
    with open(master_config_path) as f:
      build_config = yaml.load(f, Loader=yaml.FullLoader)
except:
  sys.stderr.write("Could Not Open Drop/Master Config File") 
  
try:
  with open(is_other_config_path) as d:
    is_other_config = yaml.load(d, Loader=yaml.FullLoader)
except:
  sys.stderr.write("Could Not Open IS Other Config File") 

def getYamltoDictionaryIsConfig():   
    try:
        is_env_config = open(config_path,'r')
        envConfigDictIS = yaml.safe_load(is_env_config)
    except:
        print("Could Not Open IS Config File")
    return envConfigDictIS
   
def acl_group_deployment():

  try:
    print(list(build_config.keys()))
    if 'otherisconfig' not in list(build_config.keys()): 
      #print("no is con")
      rollback_data = {}	
      with open(rollback_config_path,'w') as file:
          doc=yaml.dump(rollback_data,file)
      with open(rollback_config_path) as c:
          rollback_config_data = yaml.load(c, Loader=yaml.FullLoader)
  except:
    print(sys.exc_info())

  try:
    rollbackId= 0
    IsConfigDict=getYamltoDictionaryIsConfig()
    protocol="http"
    IShost=IsConfigDict['DeployerServer'][agent_machine]['host']
    ISPort=IsConfigDict['DeployerServer'][agent_machine]['port']    
    ISUsername=IsConfigDict['DeployerServer'][agent_machine]['user']
    server=(str(IShost)+":"+str(ISPort))
    ServiceToInvoke="VfDevOpsAutomationServices.service.pub:deployUsersGroupsACLs"
    servicePath =(sys.argv[1]+"/_edge-wmapps-deploy/wm_deploy_scripts/utils/")
    pwd_to_create_ISUser = " "
    for id in build_config['otherisconfig']:
      if id[list(id.keys())[0]]['FOR_DEPLOYMENT']=='DEPLOY':
        for key,value in id.items():
          data_list = []
          for columns, value_pair in value.items():
            if columns == 'TARGET_SERVER_ALIAS':
              env_list=[]
              target_alias_name = value_pair
              try:
                for target_alias_name in IsConfigDict[target_alias_name].keys():
                  target_alias_name = (env+"_"+target_alias_name)
                  env_list.append(target_alias_name)
                env_doclist=('%s' % ','.join((env_list)))
                doc_list_env_format = ("TARGET_SERVER_ALIAS|"+env_doclist)
              except KeyError:
                print(target_alias_name+" is not present in "+env+" config file\n")
                sys.stderr.write("Please add the above mentioned target server in respective environment IS Config file\n")                
            columns_doclist =(columns+'|'+str(value_pair))
            data_list.append(columns_doclist)
            if columns == 'ROLLBACK_ID':
              if value_pair!= None:
                rollbackId = value_pair
            if columns == 'USERNAME':
              if value_pair != None:
                for id in is_other_config['otherConfigIS']['isuser']:
                  if id[list(id.keys())[0]]['username'] == value_pair:
                    pwd_to_create_ISUser = id[list(id.keys())[0]]['password']
                    break
              else:
                pwd_to_create_ISUser = is_other_config['otherConfigIS']['isuserdefault']['password']
                break
        #print (data_list)
        java_Compile=("{}/bin/javac -cp {}wm-isclient.jar:{}vf-wm-release.jar:{}gf.javax.mail.jar:{}enttoolkit.jar {}invokeService.java".format(java_home,java_lib_path,java_lib_path,java_lib_path,java_lib_path,servicePath))
        #print(java_Compile) 
        java_Compile_Cmd= subprocess.call(shlex.split(java_Compile))
        os.chdir(servicePath)
        os.system("pwd")
        java_Exec=('{}/bin/java -cp {}wm-isclient.jar:{}vf-wm-release.jar:{}gf.javax.mail.jar:{}enttoolkit.jar invokeService {} "{}" {} {} "{}" "{ACL_NAME}" "{ACL_SERVICE}" "{ACTION}" "{ARTIFACT_TYPE}" "{ERROR_MESSAGE}" "{FOR_DEPLOYMENT}" "{GROUPNAME}" "{STATUS}" "{TARGET_SERVER_ALIAS}" "{USERNAME}" "SprintName|{SPRINT}" "LogFile|{LOGFILE}" "ReleaseName|{releasePipeline}" "PASSWORD|{password}"'.format(java_home, java_lib_path, java_lib_path, java_lib_path, java_lib_path, protocol, server, ISUsername, ISPassword, ServiceToInvoke,ACL_NAME=data_list[0],ACL_SERVICE=data_list[1],ACTION=data_list[2],ARTIFACT_TYPE=data_list[3], ERROR_MESSAGE=data_list[4],FOR_DEPLOYMENT=data_list[5], GROUPNAME=data_list[6], STATUS=data_list[8], TARGET_SERVER_ALIAS=doc_list_env_format, USERNAME=data_list[10], SPRINT=SprintName, LOGFILE=log_file, releasePipeline=releasePipelineNumber, password=pwd_to_create_ISUser ))
        #print(java_Exec, "\n\n\n")
        output=os.system(java_Exec)
        if(output == 0 or output=='0'):
            for data in build_config['otherisconfig']:
                for id in data.keys():
                  if rollbackId == id:
                      if not os.path.exists(rollback_config_path):
                          with open(rollback_config_path,'w') as file:
                              doc=yaml.dump(data,file)
                          with open(rollback_config_path) as c:
                              rollback_config_data = yaml.load(c, Loader=yaml.FullLoader)
                      else:
                          with open(rollback_config_path,'r') as file:
                              rollback_config_data = yaml.load(file, Loader=yaml.FullLoader)
                              rollback_config_data.update(data)
                          with open(rollback_config_path,'w') as yamlfile:
                              yaml.safe_dump(rollback_config_data, yamlfile) 
        else:
            #raise Exception('Return status is',output)
            print(sys.exc_info())
            sys.stderr.write("Exception occured in ACL Group deployment script")   
  except KeyError:
    print("No ACL Groups are found for this deployment")  
  except:
    print(sys.exc_info())
    sys.stderr.write("Exception occured in ACL Groups python script")              
   
  if 'otherisconfig' in build_config.keys():
    try:
      artefact_type = "ISUserGroupACLs"
      deployment_action = "DEPLOY"    
      ServiceToInvoke_Mail = "VfDevOpsAutomationServices.service.priv:sendEMailAlert"
      java_Exec=('{}/bin/java -cp {}wm-isclient.jar:{}vf-wm-release.jar:{}gf.javax.mail.jar:{}enttoolkit.jar invokeService {} "{}" {} {} "{}" "ReleaseName|{RELEASE_ID}" "SprintName|{SPRINT}" "LogFile|{LOGFILE}" "Drop|{DROP}" "ArtefactType|{ARTEFACT_TYPE}" "ActionForDeployment|{DEPLOYMENT_ACTION}" "Env|{TargetEnv}"'.format(java_home, java_lib_path, java_lib_path, java_lib_path, java_lib_path, protocol, server, ISUsername, ISPassword, ServiceToInvoke_Mail, RELEASE_ID=releasePipelineNumber, SPRINT=SprintName, LOGFILE=log_file, DROP=drop, ARTEFACT_TYPE=artefact_type, DEPLOYMENT_ACTION= deployment_action,TargetEnv= env))
      output_mail=os.system(java_Exec)
      if(output_mail == 0 or output_mail=='0'):
        print("Mail notification sent")
    except:
      print(sys.exc_info())
      
if __name__=='__main__':
    acl_group_deployment()
