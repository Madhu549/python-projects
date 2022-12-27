#importing the required module
import os
import sys
import traceback
from colorama import Fore

#taking system arguments from user
devops_shared_path = sys.argv[1]
release_name = sys.argv[2]

#framing variables
global_variables_path = f'{devops_shared_path}/globalVariableLogs'
key_store_path = f'{devops_shared_path}/keyStoreLogs'
cache_manager_path = f'{devops_shared_path}/cacheManagerLogs'

#key store file paths
keystore_deployment_completed_items_path = f'{key_store_path}/{release_name}_completed_deployment_key_stores.log'
keystore_deployment_failed_items_path = f'{key_store_path}/{release_name}_failed_deployment_key_stores.log'
keystore_rollback_completed_items_path = f'{key_store_path}/{release_name}_completed_rollback_key_stores.log'
keystore_rollback_failed_items_path = f'{key_store_path}/{release_name}_failed_rollback_key_stores.log'

#cache manager file paths
cache_manager_deployment_completed_items_path = f'{cache_manager_path}/{release_name}_completed_deployment_cache_managers.log'
cache_manager_deployment_failed_items_path = f'{cache_manager_path}/{release_name}_failed_deployment_cache_managers.log'
cache_manager_rollback_completed_items_path = f'{cache_manager_path}/{release_name}_completed_rollback_cache_managers.log'
cache_manager_rollback_failed_items_path = f'{cache_manager_path}/{release_name}_failed_rollback_cache_managers.log'

#global variable file paths
global_variables_deployment_completed_items_path = f'{global_variables_path}/{release_name}_completed_deployment_global_variables.log'
global_variables_deployment_failed_items_path = f'{global_variables_path}/{release_name}_failed_deployment_global_variables.log'
global_variables_rollback_completed_items_path = f'{global_variables_path}/{release_name}_completed_rollback_global_variables.log'
global_variables_rollback_failed_items_path = f'{global_variables_path}/{release_name}_failed_rollback_global_variables.log'



#function to print color output
def print_error(message):
    print(Fore.RED + message)
    sys.stderr.write(message)

#function to print color output
def print_success(message):
    print(Fore.GREEN + message)

#function to delete the temporary files
def delete_temp_files(path):
    if not os.path.exists(path):
        raise FileNotFoundError('file does not exist')
    os.remove(path)
    print_success(f'{path} has been deleted')


#looping through file list and delete the existing ones
file_list = [keystore_deployment_completed_items_path, keystore_deployment_failed_items_path, keystore_rollback_completed_items_path, keystore_rollback_failed_items_path, cache_manager_deployment_completed_items_path, cache_manager_deployment_failed_items_path, cache_manager_rollback_completed_items_path, cache_manager_rollback_failed_items_path, global_variables_deployment_completed_items_path, global_variables_deployment_failed_items_path, global_variables_rollback_completed_items_path, global_variables_rollback_failed_items_path]
for each_filepath in file_list:
    try:
        delete_temp_files(each_filepath)
    except Exception as e:
        traceback.print_exc()
        print_error(e)