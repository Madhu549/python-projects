import sys
import yaml
import os, subprocess, shlex, traceback
from generate_log_files import generate_log_files
sys.path.insert(1, f'{sys.argv[1]}/_edge-wmapps-deploy/wm_deploy_scripts/python_deploy_scripts/common_scripts')
# from insert_wm_release_log import insert_wm_release_log
from send_email_alert import send_email_alert

#Initializing command line arguments
sys_working_dir = sys.argv[1]
env = sys.argv[2]
java_home = sys.argv[3]
drop = sys.argv[4]
agent_machine = str(sys.argv[5])
release_name = sys.argv[6]
drop_config_path = sys.argv[7]
master_config_path = sys.argv[8]
ISPassword = sys.argv[9]
for_deployment = sys.argv[10]
other_config_path = sys.argv[11]
sprint = sys.argv[12]
redeploy_flag = sys.argv[13]
db_bkp_shared_path = sys.argv[14]
release_type = sys.argv[15]

#Assigning Path variables
repository_path = '_edge-wmapps-deploy/wm_deploy_scripts'
config_path = f'{sys_working_dir}/{repository_path}/config_files'
java_lib_path = f'{sys_working_dir}/{repository_path}/utils/wM-Dependency-Jar/'
servicePath = f'{sys_working_dir}/{repository_path}/utils/'
Is_config_path=f'{config_path}/{env}/is_config.yaml'
log_file_path = f'{sys_working_dir}/globalVariable_deployment_status.log'
devops_db_config_path = f'{config_path}/devops/db_config.yaml'

#Assigning log paths to corresponding variables
devops_shared_path = f'{db_bkp_shared_path}/globalVariableLogs'
deployment_completed_items_path = f'{devops_shared_path}/{release_name}_completed_deployment_global_variables.log'
deployment_failed_items_path = f'{devops_shared_path}/{release_name}_failed_deployment_global_variables.log'
rollback_completed_items_path = f'{devops_shared_path}/{release_name}_completed_rollback_global_variables.log'
rollback_failed_items_path = f'{devops_shared_path}/{release_name}_failed_rollback_global_variables.log'

artifact_type = 'isglobalvariable'

#Print error messages
def print_error_and_exit(error_message):
    print(error_message)
    sys.stderr.write(error_message)
    sys.exit(0)

#Sorting on precedence
def sort_on_precedence(items, reversal = False):
    drops = list(set([x[list(x.keys())[0]]['DROP_NO'] for x in items]))
    drops = sorted(drops, reverse = reversal)
    sorted_list = []
    for drop in drops:
        temp = [x for x in items if x[list(x.keys())[0]]['DROP_NO'] == drop]
        temp = sorted(temp, key=lambda x: x[list(x.keys())[0]]['ARTIFACT_PRECEDENCE'])
        sorted_list.extend(temp)
    return sorted_list

#Drop/Master yaml loading
def yaml_loader(path, error_message):
    try:
        with open(path, 'r') as f:
            build_config = yaml.load(f, Loader= yaml.FullLoader)
            return build_config
    except:
        traceback.print_exc()
        print_error_and_exit(error_message)

#Checking drop value to decide whichhh path to load(Drop/Master)     
try:
    if(drop == 'true'):
        build_config = yaml_loader(drop_config_path, "Error while loading drop_config.yaml")
        print("build_config formed from drop config yaml file...")
    else:
        build_config = yaml_loader(master_config_path, "Error while loading drop_config.yaml")
        print("build_config formed from master config yaml file...")
except:
    print_error_and_exit("Error while loading drop/master config.")

#Return list of art acts in file
def list_artifacts_in_file(path):
    try:
        with open(path, 'r') as f:
            data = f.readlines()
        records = dict({})
        for record in data:
            record = record.split('    ')
            if record[0] in records.keys():
                records[record[0]] = f"{record[1].strip()},{records[record[0]]}"
            else:
                records[record[0]] = record[1].strip()
        return records
    except:
        traceback.print_exc()
        print_error_and_exit("Execption while forming records from files....")
        

#Return list of rollback artifacts based on completed artifacts in deployment
def list_rollback_artifacts(path):
    try:
        completed_records = list_artifacts_in_file(path)
        completed_artifacts = list(completed_records.keys())
        rollback_artifacts = []
        for completed_artifact in completed_artifacts:
            deploy_artifacts = [x for x in build_config['isglobalvariable'] if x[list(x.keys())[0]]['FOR_DEPLOYMENT'] == 'DEPLOY']
            completed_dicts = [x for x in deploy_artifacts if list(x.keys())[0] == completed_artifact]
            if len(completed_artifacts) > 0:
                completed_artifact_dict = completed_dicts[0]
                rollback_artifacts.append(completed_artifact_dict[list(completed_artifact_dict.keys())[0]]['FOR_ROLLBACK'])
            else:
                print_error_and_exit(f"{completed_artifact} not found in drop/master config..")
        print(rollback_artifacts)
        rollback_records = dict({})
        for index in range(len(rollback_artifacts)):
            rollback_records[rollback_artifacts[index]] = list(completed_records.values())[index]
        return rollback_records
    except:
        traceback.print_exc()
        print_error_and_exit("Execption occured while retriving rollback artifacts for completed artifacts in deployment stage...")
        
#Changing targets in global_variables
def change_targets(global_variables, records):
    try:
        for global_variable in global_variables:
            global_variable[list(global_variable.keys())[0]]['TARGET_SERVER_ALIAS'] = records[list(global_variable.keys())[0]]
        return global_variables
    except:
        traceback.print_exc()
        print_error_and_exit("Execption occured while changing targets...")
        
#Build global global_variables
def build_global_variables(path, condition = 'false'):
    try:
        if(condition == 'false'):
            records = list_artifacts_in_file(path)
        else:
            records = list_rollback_artifacts(path)
        global_variables = [x for x in build_config['isglobalvariable'] if x[list(x.keys())[0]]['FOR_DEPLOYMENT'] == for_deployment and list(x.keys())[0] in list(records.keys())]
        global_variables = change_targets(global_variables, records)
        return global_variables
    except:
        traceback.print_exc()
        print_error_and_exit("Exception occured during global variable list building...")

def global_variable_deployment():
    try:   
        #Checking isglobalvariable entries in build_config
        if 'isglobalvariable' not in build_config.keys():
            print("No entries for global variable in the deployment...")
            return

        #Loading other_config.yaml
        other_config_dict = yaml_loader(other_config_path, "Error while loading other_config.yaml")
        is_config_dict = yaml_loader(Is_config_path, "Error while loading is_config.yaml")

        #Checking otherConfigGlobalVariable key in other_config.yaml
        if 'otherConfigGlobalVariable' in list(other_config_dict.keys()):
            print("otherConfigGlobalVariable entries found in other_config.yaml...")
            other_config_global_variable = other_config_dict['otherConfigGlobalVariable']
            
            #Checking current sprint in otherConfigGlobalVariable keys
            if sprint in list(other_config_global_variable.keys()):
                print(f"{sprint} global variable entries found...")
                
                #Taking global variables in build_config into a list based on for_deployment(DEPLOY/ROLLBACK) and redeploy_flag
                if redeploy_flag.lower() == 'true' and for_deployment.upper() == 'DEPLOY':
                    print("Deploying failed global variables...")
                    global_variables = build_global_variables(deployment_failed_items_path)
                    
                elif redeploy_flag.lower() == 'true' and for_deployment.upper() == 'ROLLBACK':
                    print("Rollbacking failed global variables...")
                    global_variables = build_global_variables(rollback_failed_items_path)
                    
                elif for_deployment.upper() == 'ROLLBACK':
                    print("Rollbacking successfully deployed global variables...")
                    global_variables = build_global_variables(deployment_completed_items_path, 'true')

                elif for_deployment.upper() == 'OVERALLROLLBACK':
                    print("Rollbacking the rollback entries mentioned in drop/master config..")
                    global_variables = [x for x in build_config['isglobalvariable'] if x[list(x.keys())[0]]['FOR_DEPLOYMENT'] == 'ROLLBACK']
                    
                else:
                    print("Normal Deployment...")
                    global_variables = [x for x in build_config['isglobalvariable'] if x[list(x.keys())[0]]['FOR_DEPLOYMENT'] == for_deployment]
                
                if len(global_variables) == 0:
                    print("No entries detected for global variables...")
                    return
                
                #Sort the list according to the DROP_NO
                reversal = False if for_deployment.upper() == 'DEPLOY' else True
                global_variables = sorted(global_variables, key=lambda x: x[list(x.keys())[0]]['DROP_NO'], reverse = reversal)

                #Sort according to ARTIFACT_PRECEDENCE
                global_variables = sort_on_precedence(global_variables, reversal)

                print(global_variables)
                
                #Initializing empty lists
                artifact_names_list, key_list, value_list, isSecure_list, action_list, target_list = [], [], [], [], [], []
                
                for global_variable in global_variables:
                    artifact_name = list(global_variable.keys())[0]
                    if artifact_name in list(other_config_global_variable[sprint].keys()):
                        if 'key' in list(other_config_global_variable[sprint][artifact_name].keys()):
                            action = global_variable[artifact_name]['ACTION'].upper()
                            if(action != 'DELETE'):
                                if 'value' in list(other_config_global_variable[sprint][artifact_name].keys()) and 'isSecure' in list(other_config_global_variable[sprint][artifact_name].keys()):
                                    print(f"All checks completed {artifact_name}...")
                                    value_list.append(other_config_global_variable[sprint][artifact_name]['value'].strip())
                                    isSecure_list.append(str(other_config_global_variable[sprint][artifact_name]['isSecure']).lower().strip())
                                else:
                                    print_error_and_exit(f"value and isSecure must be present in {artifact_name} for actions 'ADD' and 'UPDATE' in other_config.yaml")
                            else:
                                print(f"All checks completed {artifact_name}...")
                                value_list.append('NA')
                                isSecure_list.append('NA')
                                
                            #Appending the values to the final lists
                            key_list.append(other_config_global_variable[sprint][artifact_name]['key'].strip())
                            action_list.append(action.strip())
                            artifact_names_list.append(artifact_name.strip())
                            
                            #Appending environment to targets
                            if (for_deployment.upper() == 'DEPLOY' and redeploy_flag.lower() == 'false') or for_deployment.upper() == 'OVERALLROLLBACK':
                                targets = list(global_variable[artifact_name]['TARGET_SERVER_ALIAS'].split(','))
                                final_targets = []
                                for target in targets:
                                    tagert = target.strip()
                                    is_config_targets = list(is_config_dict[target].keys())
                                    final_targets.extend(is_config_targets)
                                targets = [f'{env}_{x}' for x in final_targets]
                                target_list.append(';'.join(targets))
                            else:
                                targets = list(global_variable[artifact_name]['TARGET_SERVER_ALIAS'].split(','))
                                targets = [x.strip() for x in targets]
                                target_list.append(';'.join(targets))
                            
                        else:
                            print_error_and_exit(f"key is not present in {artifact_name} in other_config.yaml")
                    else:
                        print_error_and_exit(f"{artifact_name} not found in other_config.yaml for {sprint}")
                    
                #Joining Lists to string
                key_list = ','.join(key_list)
                value_list = ','.join(value_list)
                isSecure_list = ','.join(isSecure_list)
                target_list = ','.join(target_list)
                action_list = ','.join(action_list)
                artifact_names_list = ','.join(artifact_names_list)

                print("Artifact Names:", artifact_names_list)
                print("Keys: ", key_list)
                #print("Values: ", value_list)
                print("Action: ", action_list)
                print("Target_List: ", target_list)
                print("isSecure_List: ", isSecure_list)
                
                #Assigning Deployer IS details
                protocol="http"
                IShost=str(is_config_dict['DeployerServer'][agent_machine]['host'])
                ISPort=str(is_config_dict['DeployerServer'][agent_machine]['port'])   
                ISUsername=is_config_dict['DeployerServer'][agent_machine]['user']
                server = f'{IShost}:{ISPort}'


                #Invoking WM Service
                ServiceToInvoke = 'VfDevOpsGlobalVariableDeployment.service.pub:performGlobalVariableDeployment'
                java_Compile = f"{java_home}/bin/javac -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar {servicePath}invokeService.java"
                java_Compile_Cmd = subprocess.call(shlex.split(java_Compile))
                os.chdir(servicePath)
                java_Exec = f'{java_home}/bin/java -cp {java_lib_path}wm-isclient.jar:{java_lib_path}vf-wm-release.jar:{java_lib_path}gf.javax.mail.jar:{java_lib_path}enttoolkit.jar invokeService {protocol} "{server}" {ISUsername} {ISPassword} "{ServiceToInvoke}" "ReleaseName|{release_name.upper()}" "ArtifactNameList|{artifact_names_list}" "ActionList|{action_list}" "KeyList|{key_list}" "ValueList|{value_list}" "IsSecureList|{isSecure_list}" "TargetList|{target_list}" "LogFile|{log_file_path}" "Env|{env}" "ArtifactType|{artifact_type}" "SprintName|{sprint}" "ReleaseName|{release_type}"'
                output = os.system(java_Exec)
                
                #Checking output from wM service
                if output == 0:
                    print('Service ran Successfully....')
                else:
                    print_error_and_exit(f"Error in outage enable/disable, return code: {output}, Failed to perform outage ACTION.")
                
                #Calling genrate log files function
                output = generate_log_files(log_file_path, for_deployment, db_bkp_shared_path, release_name)
                
                #Checking output from genrating log files function
                if output == 0:
                    print("Log files genrated successfully...")
                    
                else:
                    print_error_and_exit("Exception occured while generating log files...")
                    
                # #Calling insert_wm_release_log function
                # output = insert_wm_release_log(devops_db_config_path, log_file_path, release_name, sprint, 'isglobalvariable')
                
                # #Checking output from insert_wm_release_log
                # if output == 0:
                #     print("Logs are inserted into WM_RELEASE_LOG successfully..")
                
                # else:
                #     print_error_and_exit("Error occured during logs insertion into WM_RELEASE_CONFIG...")
                    
                #Calling send_email_alert function
                output = send_email_alert(sys_working_dir, log_file_path, env, sprint, release_name, 'IS Global Variable Deployment') 
                
                #Checking output from send_email_alert
                if output == 0:
                    print("Mail sent successfully...")
                
                else:
                    print_error_and_exit("Error occured during sending mail.")
                    
            else:
                print_error_and_exit(f"{sprint} entries not found in other_config.yaml")
        else:
            print_error_and_exit("otherConfigGlobalVariable entries not found in other_config.yaml")
    except:
        traceback.print_exc()
        print_error_and_exit("Execption happened while deploying global variables...")
        
#Calling global_variable_deployment function
global_variable_deployment()