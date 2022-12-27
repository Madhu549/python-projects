import sys
import yaml
import subprocess
import shlex
import cx_Oracle
import time
import os
import pickle
from os import path
import shutil
import traceback

#Getting input from user
environment = sys.argv[1]
drop=sys.argv[2]
sys_wrk_dir = sys.argv[3]
release=sys.argv[4]
secret_val = sys.argv[5]
db_bkp_shared_path = sys.argv[6]
release_name = sys.argv[7]
java_home=sys.argv[10]
ISPassword=sys.argv[11]
agent_machine=sys.argv[12]
drop_filter = sys.argv[13] # this variable is added for DB deployment from the failure drop
start_drop = int(sys.argv[14])
end_drop = int(sys.argv[15])

if  not ((start_drop == 0 and end_drop == 0) or (end_drop != 0 and start_drop != 0)):
  raise Exception(f'Start drop = {start_drop}\n End drop = {end_drop}\n Enter the correct values of Start drop and End drop\n')
if start_drop > end_drop:
  raise Exception(f'Start drop = {start_drop}\n End drop = {end_drop}\n Value of start drop is greater than the value of end drop\n')

base_path=(sys_wrk_dir+'/_db_artifacts/'+release)
installdb_path=(sys_wrk_dir+'/_edge-wmapps-deploy/wm_deploy_scripts/db_deploy_script')
drop_config_path= sys.argv[8]
master_config_path= sys.argv[9]
rollback_config_path = (db_bkp_shared_path+'/rollback_config.txt')
config_path=(sys_wrk_dir+'/_edge-wmapps-deploy/wm_deploy_scripts/config_files/'+ environment +'/db_config.yaml')
is_config_path =(sys_wrk_dir+'/_edge-wmapps-deploy/wm_deploy_scripts/config_files/'+ environment +'/is_config.yaml')
table_rollback_script_path=(sys_wrk_dir+'/_edge-wmapps-deploy/wm_deploy_scripts/db_deploy_script')
java_lib_path=(sys_wrk_dir+"/_edge-wmapps-deploy/wm_deploy_scripts/utils/wM-Dependency-Jar/")
backup_path = db_bkp_shared_path+'/db_csv_backup_ctl/'
success_script_txt_path = sys_wrk_dir+'/completed_scripts.txt'
failed_script_txt_path = sys_wrk_dir+'/failed_scripts.txt'
log_file_path= db_bkp_shared_path+'/db_logs/'+release_name+'.log'
db_log_publish = sys_wrk_dir+'/db_publish.log'
completed_scripts = db_bkp_shared_path+'/db_completed_scripts/'+release+'_'+environment+'_deployment_completed_scripts.txt'
success_status = 'SUCCESS'
failed_status = 'FAILURE'

 # For DB deployment from the failure drop, this path contains yaml file whcich is updated with failed artifacts list from original master config
failed_db_path = db_bkp_shared_path+'/failed_scripts/'+release+'_'+environment+'_db_failed.yaml'

'''if start_drop != 0 and end_drop == 0:
  print('1')
  raise Exception(f'Start drop = {start_drop}\n End drop = {end_drop}\n Enter the correct values of Start drop and End drop\n')
elif start_drop == 0 and end_drop != 0:
  print('2')
  raise Exception(f'Start drop = {start_drop}\n End drop = {end_drop}\n Enter the correct values of Start drop and End drop\n')
elif start_drop > end_drop:
  print('3')
  raise Exception(f'Start drop = {start_drop}\n End drop = {end_drop}\n Value of start drop is greater than the value of end drop\n')'''


temp_path = (db_bkp_shared_path+'/db_csv_backup_ctl')

if os.path.exists(rollback_config_path):
  os.remove(rollback_config_path)
else:
  print("Cannot delete db rollback config file"+rollback_config_path+"as it doesn't exists")

#check to read master or drop config
failed_db_config={}
drop_dict = {}
rollback_dict = {}
try:
  if drop == 'true':
    with open(drop_config_path) as f:
      build_config = yaml.load(f, Loader=yaml.FullLoader)
  elif os.path.exists(failed_db_path):    #It checks whether the file is there is not with failed scripts, if yes it will take that file as master
    if drop_filter.lower() == 'true':
      with open(failed_db_path,'r') as f:
        build_config=yaml.load(f,Loader=yaml.FullLoader)
      with open(failed_db_path) as f:
        failed_db_config = yaml.load(f, Loader=yaml.FullLoader)        
    else:
      with open(failed_db_path) as f:
        failed_db_config = yaml.load(f, Loader=yaml.FullLoader)
      sys.exit(1)      
  else:
    with open(master_config_path) as f:
      build_config = yaml.load(f, Loader=yaml.FullLoader)
    with open(master_config_path) as f:
      failed_db_config = yaml.load(f, Loader=yaml.FullLoader)  
except:
  traceback.print_exc()
  if os.path.exists(failed_db_path):
    with open(failed_db_path, 'w+') as outfile:
      yaml.dump(failed_db_config, outfile, default_flow_style=False)
    db_artifact_count = 'false'  
    sys.stderr.write("Master Deploymnet can't proceed since there is DB failure deployment")
  else:
    sys.stderr.write("Unable to Open Drop/Master Config File")

with open(failed_db_path, 'w+') as outfile:
  yaml.dump(failed_db_config, outfile, default_flow_style=False)    # updating the failed_db_path with copy of master

#Function to remove yaml entries based on drop and schema
def remove_script(build_config, drop, schema, type):
    found_scripts = []
    if type in build_config.keys():
        for script in build_config[type]:
            script_name = list(script.keys())[0]
            if((script[script_name]['DROP_NO']) == drop and (script[script_name]['TARGET_SERVER_ALIAS'][0] == schema)):
                found_scripts.append(script)
    for script in found_scripts:
        build_config[type].remove(script)
    return build_config

#Function to remove all entries with specific drop and schema
def remove_drop_and_schema(build_config, drop, schema):
    build_config = remove_script(build_config, drop, schema, 'db/sql')
    build_config = remove_script(build_config, drop, schema, 'db/ldr')
    build_config = remove_script(build_config, drop, schema, 'db/obj')
    return build_config

###Exit when there are no dbscripts are given for deployment#####
if not any(['db/sql' in build_config, 'db/obj' in build_config, 'db/ldr' in build_config]):
  with open(rollback_config_path, 'wb') as filehandle:
    pickle.dump(rollback_dict, filehandle)
  print('No DB artifacts found in the build config...exiting')
  sys.exit(0)


try:
  with open(config_path) as f:
      db_config = yaml.load(f, Loader=yaml.FullLoader)
except:
  traceback.print_exc()
  sys.stderr.write(f"Unable to Open DB Config File for environment:{environment}")

try:
  with open(is_config_path) as f:
      is_config = yaml.load(f, Loader=yaml.FullLoader)
except:
  traceback.print_exc()
  sys.stderr.write(f"Unable to Open IS Config File for environment:{environment}")


def decrypt_with_ansible_vault(backup_path, release_name, secret_val, environment):
  file_to_decrypt = backup_path+release_name+".zip"
  os.makedirs(backup_path+environment)
  key_file =  backup_path+environment+"/key.secret"
  f = open(key_file, "w")
  f.write(secret_val)
  f.close()
  decrypt_command = ("ansible-vault decrypt {} --vault-password-file {}".format(file_to_decrypt,key_file))
  res1 = subprocess.call(shlex.split(decrypt_command))
  print("Decrypted "+release_name+".zip successfully")
  rel_path=backup_path+release_name
  shutil.unpack_archive(file_to_decrypt, backup_path, 'zip')
  print("Unzipped "+release_name+".zip successfully")
  shutil.rmtree(backup_path+environment)

def encrypt_with_ansible_vault(backup_path, release_name, secret_val, environment):
  os.makedirs(backup_path+environment)
  key_file =  backup_path+environment+"/key.secret"
  f = open(key_file, "w")
  f.write(secret_val)
  f.close()
  file_to_encrypt = backup_path+release_name+".zip"
  print(file_to_encrypt)
  encrypt_command = ("ansible-vault encrypt {} --vault-password-file {}".format(file_to_encrypt,key_file))
  res1 = subprocess.call(shlex.split(encrypt_command))
  print("Encrypted "+release_name+".zip successfully")
  shutil.rmtree(backup_path+environment)

def reset_drop(drop):

  if drop in rollback_dict:
    print(f"Partial drop Failure triggered drop reset. Resetting db/sql of deployed scehmas in Drop {drop}...")
    reset_dict = rollback_dict[drop]
  else:
    return

  for schema in reset_dict:
    con_url = db_config[schema]['connectionurl'].rsplit('@', 1)[1]
    user_name, password = db_config[schema]['username'], db_config[schema]['password']

    if 'sql' in reset_dict[schema]:
        installdb_cmd = f"{installdb_path}/install_db.sh {user_name}/{password}@{con_url} {base_path}/{drop}/{schema}/rollback_db.txt {log_file_path} {sys_wrk_dir} {completed_scripts} Deploy"
        res = subprocess.call(shlex.split(installdb_cmd))
        if res == 0:
          reset_dict[schema].pop('sql')
        else:
          rollback_dict[drop] = reset_dict
          sys.stderr.write(f"##[eeror]Fatal: A failure has occured while resetting sql of drop {drop}, schema {schema}. Please reset the drop manually before starting redeployment, please check logs for reason of failure")
          return
  rollback_dict[drop] = reset_dict

if 'db/sql' in list(build_config.keys()):

  for db_package in build_config['db/sql']:
    for key in db_package.keys():
      if db_package[key]['DROP_NO'] in drop_dict.keys():
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          if schema_name not in drop_dict[db_package[key]['DROP_NO']]:
            drop_dict[db_package[key]['DROP_NO']][schema_name] = {}

          if 'sql' not in drop_dict[db_package[key]['DROP_NO']][schema_name].keys():
            drop_dict[db_package[key]['DROP_NO']][schema_name]['sql']={}
      else:
        drop_dict[db_package[key]['DROP_NO']] ={}
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          drop_dict[db_package[key]['DROP_NO']][schema_name] = {}
          drop_dict[db_package[key]['DROP_NO']][schema_name]['sql']={}


if 'db/ldr' in list(build_config.keys()):
  for db_package in build_config['db/ldr']:
    for key in db_package.keys():
      if db_package[key]['DROP_NO'] in drop_dict.keys():
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          if schema_name not in drop_dict[db_package[key]['DROP_NO']]:
            drop_dict[db_package[key]['DROP_NO']][schema_name] = {}

          if 'ldr' not in drop_dict[db_package[key]['DROP_NO']][schema_name].keys():
            drop_dict[db_package[key]['DROP_NO']][schema_name]['ldr']={}
      else:
        drop_dict[db_package[key]['DROP_NO']] ={}
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          drop_dict[db_package[key]['DROP_NO']][schema_name] = {}
          drop_dict[db_package[key]['DROP_NO']][schema_name]['ldr']={}
      for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
        if 'ldr' in list(drop_dict[db_package[key]['DROP_NO']][schema_name].keys()):
           drop_dict[db_package[key]['DROP_NO']][schema_name]['ldr'][key] = db_package[key]['BACKUP_ARTIFACTNAME']


if 'db/obj' in list(build_config.keys()):
  for db_package in build_config['db/obj']:
    for key in db_package.keys():
      if db_package[key]['DROP_NO'] in drop_dict.keys():
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          if schema_name not in drop_dict[db_package[key]['DROP_NO']]:
            drop_dict[db_package[key]['DROP_NO']][schema_name] = {}

          if 'obj' not in drop_dict[db_package[key]['DROP_NO']][schema_name].keys():
            drop_dict[db_package[key]['DROP_NO']][schema_name]['obj']={}
      else:
        drop_dict[db_package[key]['DROP_NO']] ={}
        for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
          drop_dict[db_package[key]['DROP_NO']][schema_name] = {}
          drop_dict[db_package[key]['DROP_NO']][schema_name]['obj']={}
      for schema_name in db_package[key]['TARGET_SERVER_ALIAS']:
       if 'obj' in list(drop_dict[db_package[key]['DROP_NO']][schema_name].keys()):
        drop_dict[db_package[key]['DROP_NO']][schema_name]['obj'][key] = db_package[key]['BACKUP_ARTIFACTNAME']
  print("drop_dict in obj:", drop_dict)

sorted_drop_list = sorted(drop_dict.keys())




"""if drop_filter.lower() == "true":
  with open(failed_db_path) as f:
      sorted_drop_list = yaml.load(f, Loader=yaml.FullLoader)
  if drop_filter.isnumeric() and int(drop_filter) == min(sorted_drop_list):
    drop_filter = int(drop_filter)
    sorted_drop_list = filter(lambda x: x >= drop_filter, sorted_drop_list)
  else:
    raise Exception(f"##[error]Invalid value in Drop filter variable. It should be None as default or between and inlcuding {min(sorted_drop_list)} -  {max(sorted_drop_list)}. ")
"""
db_artifact_count = 'true' #taking a flag reference for confirmation of successfull deployment
try:
  for i in sorted_drop_list:
    if (start_drop == 0 and end_drop == 0) or (i >= start_drop and i <= end_drop):
        print('entering in to condion ')
        print(f'start_drop: {start_drop} and end_drop: {end_drop} and drop_number: {i}')
        for schema_name in drop_dict[i].keys():
          if 'sql' in drop_dict[i][schema_name].keys():
            db_artifact_count = 'false'        
            con_url=(str(db_config[schema_name]['connectionurl']).rsplit('@', 1)[1])
            installdb_cmd=('{}/install_and_rollback_db.sh "{}/{}@{}" {}/{}/{}/db.txt {} {}'.format(installdb_path,db_config[schema_name]['username'],db_config[schema_name]['password'],con_url,base_path,i,schema_name,log_file_path,sys_wrk_dir))
            res=subprocess.call(shlex.split(installdb_cmd))
            print("res is in sql:"+str(res))
            if res == 1:
                reset_drop(i)
                sys.exit(2)
                break
            if '0' in str(res):
              if i in rollback_dict.keys():
                if schema_name not in rollback_dict[i]:
                  rollback_dict[i][schema_name] = {}

                  if 'sql' not in rollback_dict[i][schema_name].keys():
                    rollback_dict[i][schema_name]['sql'] = {}
              else:
                  rollback_dict[i] = {}
                  rollback_dict[i][schema_name] = {}
              rollback_dict[i][schema_name]['sql'] = {}

              if path.exists(success_script_txt_path):
                file1 = open(success_script_txt_path,"r")
                scripts_txt = file1.readlines()
              else:
                print("completed_scripts.txt file is not present")
                
              for each_sql in scripts_txt:
                artifact_name=(each_sql.rsplit('/', 1)[1]).strip()
                log_content = ('{}/{}/{}/sql/{}    {}    {}    successfully deployed\n'.format(release,i,schema_name,artifact_name,schema_name,success_status))              
                f=open(db_log_publish, "a+")
                f.write(log_content)
                f.close()
                with open(failed_db_path, 'r') as fl:              
                  toDelete=yaml.safe_load(fl)
                if toDelete.get('db/sql') is not None:
                  for j in toDelete['db/sql']:
                    if list(j.keys())[0] == artifact_name:
                      toDelete['db/sql'].remove(j)        # removing the artifact from the copy of master which is located in shared path which is success in master
                      break
                  setDeleted= toDelete.copy()
                  with open(failed_db_path,'w+') as of:
                    yaml.dump(setDeleted,of,default_flow_style=False)
                  db_artifact_count = 'true'
                         
            if '2' in str(res):
              if path.exists(failed_script_txt_path):
                file2 = open(failed_script_txt_path,"r")
                failed_scripts_txt = file2.readlines()
              else:
                print("failed_scripts.txt file is not present")
              for each_sql_fail in failed_scripts_txt:
                failed_artifact_name=(each_sql_fail.rsplit('/', 1)[1]).strip()
                failed_log_content = ('{}/{}/{}/sql/{}    {}    {}    script failed,please check log file\n'.format(release,i,schema_name,failed_artifact_name,schema_name,failed_status))
                f=open(db_log_publish, "a+")
                f.write(failed_log_content)
                f.close()
              sys.stderr.write("Error occured during installing sql script....")
              reset_drop(i)
              sys.exit(2)
              break
          failed_db_config=remove_script(failed_db_config,i,schema_name,'db/sql')
          with open(failed_db_path,'w+') as of:
            yaml.dump(failed_db_config,of,default_flow_style=False)
        for schema_name in drop_dict[i].keys():
          if 'ldr' in drop_dict[i][schema_name].keys():
            db_artifact_count = 'false'
            dsn = (db_config[schema_name]['connectionurl']).split('@')[1] #Splitting connection URL
            dsn_form1 = dsn.replace('(','\(')
            dsn_form2 = dsn_form1.replace(')','\)')
            dsn_form3 = dsn_form2.replace('=','\=')
            dsn_form4 = '\\"'+dsn_form3+'\\"'
            for file_name in drop_dict[i][schema_name]['ldr'].keys():
              ctl_file = ("{}/_db_artifacts/{}/{}/{}/ldr/{}").format(sys_wrk_dir, release, str(i), schema_name, file_name)
              execute_ldr = ("sqlldr {}/{}@{} {}".format(db_config[schema_name]['username'],db_config[schema_name]['password'],dsn_form4,ctl_file))
              deploy_result=subprocess.call(shlex.split(execute_ldr))
              print("result in ldr: ",deploy_result)
              ctl_log_path='./'+(file_name.split('.ctl')[0])+'.log'
              if path.isfile(ctl_log_path):
                  print('Printing {} content'.format(ctl_log_path))
                  ctl_log_file = open(ctl_log_path)
                  lines_log = ctl_log_file.readlines()
                  for line_log in lines_log:
                    print(line_log)
              if deploy_result == 0:
                if i in rollback_dict.keys():
                  if schema_name not in rollback_dict[i]:
                    rollback_dict[i][schema_name]={}
                  if 'ldr' not in rollback_dict[i][schema_name].keys():
                    rollback_dict[i][schema_name]['ldr'] = {}
                else:
                  rollback_dict[i] = {}
                  rollback_dict[i][schema_name]={}
                  rollback_dict[i][schema_name]['ldr']={}
                if 'ldr' in list(rollback_dict[i][schema_name].keys()):
                  rollback_dict[i][schema_name]['ldr'][file_name] = drop_dict[i][schema_name]['ldr'][file_name]                
                log_content_ldr = ('{}/{}/{}/ldr/{}    {}    {}    successfully deployed\n'.format(release,i,schema_name,file_name,schema_name,success_status))              
                f=open(db_log_publish, "a+")
                f.write(log_content_ldr)
                f.close()
                with open(failed_db_path, 'r') as fl:
                  toDelete=yaml.safe_load(fl)
                if toDelete.get('db/ldr') is not None:
                  for j in toDelete['db/ldr']:
                    if list(j.keys())[0] == file_name:
                      toDelete['db/ldr'].remove(j)       # removing the artifact from the copy of master which is located in shared path which is success in master
                      break
                  setDeleted= toDelete.copy()
                  with open(failed_db_path,'w+') as of:
                    yaml.dump(setDeleted,of,default_flow_style=False)
                  db_artifact_count = 'true'  
                
                  

              if deploy_result!=0:
                print("Ctl file failed:",file_name)
                decrypt_with_ansible_vault(backup_path, release_name, secret_val, environment)
                path_var=("{}/{}/{}/{}/{}/").format(temp_path, release_name, release, i, schema_name)
                csv_filename=str(path_var+"/"+drop_dict[i][schema_name]['ldr'][file_name]+"_backupfile.csv")

                rollback_cmd=("{}/table_rollback.sh {}/{}@{} {} {}".format(table_rollback_script_path,db_config[schema_name]['username'],db_config[schema_name]['password'],dsn_form4,csv_filename,db_config[schema_name]['username']))
                if str(path.isfile(csv_filename)) == 'True':
                  print("csv_filename: " + csv_filename + " is Available")
                else:
                  print("csv_filename: " + csv_filename + " is NOT Available")
                rollback_result=subprocess.call(shlex.split(rollback_cmd))
                print("rollback_result in ldr: ",rollback_result)

                reset_drop(i)
                with open(rollback_config_path, 'wb') as filehandle:
                  pickle.dump(rollback_dict, filehandle)

                failed_log_content_ldr = ('{}/{}/{}/ldr/{}    {}    {}    script failed,please check log file\n'.format(release,i,schema_name,file_name,schema_name,failed_status))
                f=open(db_log_publish, "a+")
                f.write(failed_log_content_ldr)
                f.close()

                sys.stderr.write("Error occured during ctl deployment....")
                sys.exit()
          failed_db_config=remove_script(failed_db_config,i,schema_name,'db/ldr')
          with open(failed_db_path,'w+') as of:
            yaml.dump(failed_db_config,of,default_flow_style=False)
        for schema_name in drop_dict[i].keys():
          if 'obj' in drop_dict[i][schema_name].keys():
            db_artifact_count = 'false'
            print("schema name in db/obj:",schema_name)
            con_url=(str(db_config[schema_name]['connectionurl']).rsplit('@', 1)[1])
            installdb_cmd=('{}/install_db.sh "{}/{}@{}" {}/{}/{}/db_obj.txt {} {} {} {}'.format(installdb_path,db_config[schema_name]['username'],db_config[schema_name]['password'],con_url,base_path,i,schema_name,log_file_path,sys_wrk_dir,completed_scripts,'Deploy' ))
            res=subprocess.call(shlex.split(installdb_cmd))
            print("res in obj:"+str(res))
            if '2' in str(res):
              reset_drop(i)
              sys.stderr.write("Error occured during obj deployment....please check log file")
              quit()
            if '0' in str(res):
              if path.exists(success_script_txt_path):
                file_obj=open(success_script_txt_path,"r")
                scripts_txt_obj_log = file_obj.readlines()
              else:
                print("completed_scripts.txt file is not present")
              for each_sql in scripts_txt_obj_log:
                artifact_name_obj_log=(each_sql.rsplit('/', 1)[1]).strip()
                log_content_obj = ('{}/{}/{}/obj/{}    {}    {}    successfully deployed\n'.format(release,i,schema_name,artifact_name_obj_log,schema_name,success_status))              
                f=open(db_log_publish, "a+")
                f.write(log_content_obj)
                f.close()
                with open(failed_db_path, 'r') as fl:
                  toDelete=yaml.safe_load(fl)
                if toDelete.get('db/obj') is not None:
                  for j in toDelete['db/obj']:
                    if list(j.keys())[0] == artifact_name_obj_log:
                      toDelete['db/obj'].remove(j)              # removing the artifact from the copy of master which is located in shared path which is success in master
                      break
                  setDeleted= toDelete.copy()
                  with open(failed_db_path,'w+') as of:
                    yaml.dump(setDeleted,of,default_flow_style=False)
                  db_artifact_count = 'true'  
                
            if '2' in str(res):
              if path.exists(failed_script_txt_path):
                file2_obj = open(failed_script_txt_path,"r")
                failed_scripts_txt_obj = file2_obj.readlines()
              else:
                print("failed_scripts.txt file is not present")
              for each_sql_obj in failed_scripts_txt_obj:
                failed_artifact_name_obj=(each_sql_obj.rsplit('/', 1)[1]).strip()
                failed_log_content_obj = ('{}/{}/{}/obj/{}    {}    {}    script failed,please check log file\n'.format(release,i,schema_name,failed_artifact_name_obj,schema_name,failed_status))
                f=open(db_log_publish, "a+")
                f.write(failed_log_content_obj)
                f.close()

            if path.exists(success_script_txt_path):
              file1 = open(success_script_txt_path,"r")
              scripts_txt = file1.readlines()
            else:
              sys.stderr.write("completed_scripts.txt file is not present")
            for each_sql in scripts_txt:
              artifact_name=(each_sql.rsplit('/', 1)[1]).strip()
              if i in rollback_dict.keys():
                if schema_name not in rollback_dict[i]:
                  rollback_dict[i][schema_name]={}
                if 'obj' not in rollback_dict[i][schema_name].keys():
                  rollback_dict[i][schema_name]['obj'] = {}
              else:
                rollback_dict[i] = {}
                rollback_dict[i][schema_name]={}
                rollback_dict[i][schema_name]['obj']={}
              if 'obj' in list(rollback_dict[i][schema_name].keys()):
                rollback_dict[i][schema_name]['obj'][artifact_name] = drop_dict[i][schema_name]['obj'][artifact_name]
          failed_db_config=remove_script(failed_db_config,i,schema_name,'db/obj')
          with open(failed_db_path,'w+') as of:
            yaml.dump(failed_db_config,of,default_flow_style=False)
              
except :
  traceback.print_exc()
  sys.stderr.write("Error or Exception occured while installing db scripts...search logs using the word traceback to see what went wrong...")

     
finally:
  print("Db artifact count status : "+db_artifact_count) #Printing the status of the db_artifact_count variable like true or false
  if db_artifact_count == 'true':
    os.remove(failed_db_path)        #Deleting the file which is created while doing the deployment for the reference of failed drops since deployment got success
  with open(rollback_config_path, 'wb') as filehandle:
    pickle.dump(rollback_dict, filehandle)
  print("Successfully deployed in: ",rollback_dict)
  try:

    if path.isfile(log_file_path):
      log_db = open(log_file_path)
      lines_db = log_db.readlines()
      for line_db in lines_db:
        print("db log file content in shared dir:",line_db)
    if path.isfile(db_log_publish):
      log = open(db_log_publish)
      lines = log.readlines()
      for line in lines:
        print("mail publish log content:",line)
      artefact_type = "db"
      deployment_action = "DEPLOY"
      ServiceToInvoke_Mail = "VfDevOpsAutomationServices.service.priv:sendEMailAlert"
      protocol="http"
      IShost=is_config['DeployerServer'][agent_machine]['host']
      ISPort=is_config['DeployerServer'][agent_machine]['port']
      ISUsername=is_config['DeployerServer'][agent_machine]['user']
      server=(str(IShost)+":"+str(ISPort))
      servicePath =(sys_wrk_dir+"/_edge-wmapps-deploy/wm_deploy_scripts/utils/")
      java_Compile=("{}/bin/javac -cp {}wm-isclient.jar:{}vf-wm-release.jar:{}gf.javax.mail.jar:{}enttoolkit.jar {}invokeService.java".format(java_home,java_lib_path,java_lib_path,java_lib_path,java_lib_path,servicePath))
      java_Compile_Cmd= subprocess.call(shlex.split(java_Compile))
      os.chdir(servicePath)
      java_Exec=('{}/bin/java -cp {}wm-isclient.jar:{}vf-wm-release.jar:{}gf.javax.mail.jar:{}enttoolkit.jar invokeService {} "{}" {} {} "{}" "ReleaseName|{RELEASE_ID}" "SprintName|{SPRINT}" "LogFile|{LOGFILE}" "Drop|{DROP}" "ArtefactType|{ARTEFACT_TYPE}" "ActionForDeployment|{DEPLOYMENT_ACTION}" "Env|{ENVIRONMENT}"'.format(java_home, java_lib_path, java_lib_path, java_lib_path, java_lib_path, protocol, server, ISUsername, ISPassword, ServiceToInvoke_Mail, RELEASE_ID=release_name, SPRINT=release, LOGFILE=db_log_publish, DROP=drop, ARTEFACT_TYPE=artefact_type, DEPLOYMENT_ACTION= deployment_action, ENVIRONMENT=environment))
      output=os.system(java_Exec)
      if(output == 0 or output=='0'):
        print("Mail notification sent for DB log")
  except:
    traceback.print_exc()
