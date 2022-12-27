#importing required modules
from distutils.version import Version
import warnings
warnings.filterwarnings("ignore")
import shlex
import zipfile
import os
import traceback
import shutil
import subprocess
import pandas as pd
import re
import yaml
import sys
import xmltodict
import re
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from colorama import Fore
from pathlib import Path

#Importing utils
sys.path.insert(1, f'{sys.argv[1]}/_webMethods-Upgrade/python/utils')
from decrypt_hostvars import DecryptHostvars

#System arguments assignment
system_working_directory = sys.argv[1]
secret_value = sys.argv[2]
source_environment = sys.argv[3]
target_environment = sys.argv[4]
zone = sys.argv[5]
instance = sys.argv[6]

def print_error(message):
    print(Fore.RED + message)
    sys.stderr.write(message)
    
def print_success(message):
    print(Fore.GREEN + message)

class ACLComparison:

    #Constructor
    def __init__(self, source_environment,target_environment, source_instance, target_instance, source_host, target_host, system_working_directory):
        
        self.source_environment = source_environment
        self.target_environment = target_environment
        self.source_instance = source_instance
        self.target_instance = target_instance
        self.source_host = source_host
        self.target_host = target_host
        self.system_working_directory = system_working_directory
        self.source_alias_list = self.source_instance.split('_')
        self.target_alias_list = self.target_instance.split('_')
        self.source_inventory = f"{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{self.source_environment}/hosts"
        self.target_inventory = f"{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{self.target_environment}/hosts"
        
        #Forming extracting folder names for packages
        self.extracted_packages_source = f"{self.system_working_directory}/extracted_packages_source"
        self.extracted_packages_target = f"{self.system_working_directory}/extracted_packages_target"

        #Forming extracting folder names for cnf
        self.extracted_cnf_source = f"{self.system_working_directory}/extracted_cnf_source"
        self.extracted_cnf_target = f"{self.system_working_directory}/extracted_cnf_target"
        
        #Forming packages zip file names
        self.source_packages_path = f"{self.source_host}"
        self.source_cnf_path = f"{self.source_host}"
        self.target_packages_path = f"{self.target_host}"
        self.target_cnf_path = f"{self.target_host}"
        
        print_success("Comparison object Successfully Initialized...")
        
    def invoke_play_command(self, play_path, hostname, inventory, instance, file_name, acl_file_name, type):
        
        play_command = f'ansible-playbook {play_path} -i {inventory} -e server={hostname}  --extra-vars "instance={instance} file_name={file_name} acl_file_name={acl_file_name} type={type} swd={self.system_working_directory}"'
        print(play_command)
        return subprocess.run(shlex.split(play_command))
    
    #Fecthing package folders from source and target servers 
    def fetch_package_folders(self):
        source_type = 'source'
        target_type = 'target'
        
        play_path = f"{self.system_working_directory}/_webMethods-Upgrade/playbooks/acl_comparision/acl_comparision.yaml"
        output = self.invoke_play_command(play_path, self.source_host, self.source_inventory, self.source_alias_list[2], self.source_packages_path, self.source_cnf_path, source_type)
        print("Source Playbook Output: ", output)
        output = self.invoke_play_command(play_path, self.target_host, self.target_inventory, self.target_alias_list[2], self.target_packages_path, self.target_cnf_path, target_type)
        print("Target Playbook Output: ", output)
        print_success("Fetching packages completed....")
     
    #Unzipping package folder function
    def unzip_package_folders(self):
        
        source_package_path = f"{self.system_working_directory}/buffer/{self.source_packages_path}.zip"
        target_package_path = f"{self.system_working_directory}/buffer/{self.target_packages_path}.zip"
        source_acl_path = f"{self.system_working_directory}/buffer/{self.source_cnf_path}"
        target_acl_path = f"{self.system_working_directory}/buffer/{self.target_cnf_path}"
        
        #Unzipping source packages folder
        with zipfile.ZipFile(source_package_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_source)
            
        #Unzipping target packages folder
        with zipfile.ZipFile(target_package_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_target)

         

            
        print_success("Unzipping package and cnf folders is successfully completed...")

    #Fecthing packages list from source packages folders
    def fetch_packages_list(self, type):
        
        print(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        packages_list = os.listdir(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        temporary_list = packages_list[:]
        a = f'no_manifest_packages_{type}'
        a = []
        
        for package in temporary_list:
            if (os.path.isdir(f"{self.system_working_directory}/extracted_packages_{type}/packages/{package}") == False) or (re.match('^Wm', package)) or (re.match('$.txt', package)):
                packages_list.remove(package)
            if (re.match('^Wm', package)):
                a.append(package)
                
            
        print(f"Successfully fetched packages names for type: {type}")
        
        return packages_list, a


    #fetching cnf files from the extracted cnf folders
    def fetch_cnf_files(self, type):
        print(f"{self.system_working_directory}/extracted_cnf_{type}")
        cnf_name_list = os.listdir(f"{self.system_working_directory}/extracted_cnf_{type}")

        return cnf_name_list
    
    def return_value_status(self, values):
        try:
            value = values['#text']
            if value == 'yes':
                return 'Enabled'
            else:
                return 'Disabled'
        except KeyError:
            return 'NA'

    #Method to fetch the package_version and package_status
    def fetch_status(self, package_name, type):
        
        if type == 'target':
            extracted_path = self.extracted_packages_target
        else:
            extracted_path = self.extracted_packages_source
        
        package_path = f"{extracted_path}/packages/{package_name}"
        
        if os.path.exists(package_path):
            try:
                with open(f'{package_path}/manifest.v3', 'r') as f:
                    xml_data = f.read()
            
            except:
                return 1

            xml_dict = xmltodict.parse(xml_data)

            enabled_flag = True

            for values in xml_dict['Values']['value']:
                if values['@name'] == 'enabled':
                    enabled_flag = False
                    status = self.return_value_status(values)
                
            if enabled_flag:
                status = 'NA'    
                
            return f"{status}"

        else:
            return 1


    #fetching acl elements and their associatedvalues from cnf file
    def fetch_acl_elements(self, package_name, cnf_name, type):
        acl_dict = {}
        acl_element_list = []
        acl_element_value_list = []
        new_acl_element_list = []  
        
        if type == 'target':
            extracted_path = self.extracted_cnf_target
        else:
            extracted_path = self.extracted_cnf_source
        
        cnf_path = f"{extracted_path}/{cnf_name}"

        if os.path.exists(cnf_path):
            try:
                with open(f'{cnf_path}', 'r') as f:
                    xml_data = f.read()    
            except:
                return 1

            xml_dict = xmltodict.parse(xml_data)

            package_names = xml_dict['Values']['value']

            for i in range(len(package_names)):
                acl_name = xml_dict['Values']['value'][i]['@name']
                acl_value = xml_dict['Values']['value'][i]['#text']
                acl_dict[acl_name] = acl_value


            for key in acl_dict:
                acl_element_list.append(key)
                
            acl_element_list.sort()
            for i in acl_element_list:
                if i.split('.')[0] == package_name:
                    new_acl_element_list.append(i[:])
                    acl_element_value_list.append(acl_dict[i])

        return new_acl_element_list, acl_element_value_list


    #removing data from the buffer    
    def remove_buffer_directories(self):
        try:
            shutil.rmtree(self.extracted_packages_source)
            shutil.rmtree(self.extracted_packages_target)
            shutil.rmtree(self.extracted_cnf_source)
            shutil.rmtree(self.extracted_cnf_target)
            shutil.rmtree(f"{self.system_working_directory}/buffer")
            print("Buffer directories removed.")
        except:
            traceback.print_exc()
            print("Exception while removing buffer directories.")

def check_environment(environment):
    environemnt_list = ['dev_10.1', 'sit3_10.1', 'sit4_10.1', 'cob1_pr_10.1', 'cob1_sw_10.1', 'cob2_pr_10.1', 'cob2_sw_10.1']
    if environment in environemnt_list:
        print_success("Environemnt is valid. Contuining with flow.")
        return 0
    else:
        print(f"Invalid environment detected. Environment must be in the list of {environemnt_list}.")
        return 1

def fetch_source_and_target_alias():
    
    source_zone_and_instance_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{source_environment}/zone_and_instance.yaml'
    target_zone_and_instance_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{target_environment}/zone_and_instance.yaml'
    
    with open(source_zone_and_instance_path, 'r') as f:
        source_data = yaml.load(f, Loader=yaml.FullLoader)
    with open(target_zone_and_instance_path, 'r') as f:
        target_data = yaml.load(f, Loader=yaml.FullLoader)
    
    source_and_target_alias = []
    source_env = source_environment.split('_')[0]
    target_env = target_environment.split('_')[0]
    if zone.upper() == 'ALL':
        for each_zone in source_data.keys():
            for each_instance in source_data[each_zone]['instances']:
                temp_list = []
                temp_list.append({f'{source_env}_{each_zone}_{each_instance}': source_data[each_zone]['alias']})
                temp_list.append({f'{target_env}_{each_zone}_{each_instance}': target_data[each_zone]['alias']})
                source_and_target_alias.append(temp_list)
    else:
        if instance.upper() == 'ALL':
            for each_instance in source_data[zone]['instances']:
                temp_list = []
                temp_list.append({f'{source_env}_{zone}_{each_instance}': source_data[zone]['alias']})
                temp_list.append({f'{target_env}_{zone}_{each_instance}': target_data[zone]['alias']})
                source_and_target_alias.append(temp_list)
        else:
            temp_list = []
            temp_list.append({f'{source_env}_{zone}_{instance}': source_data[zone]['alias']})
            temp_list.append({f'{target_env}_{zone}_{instance}': target_data[zone]['alias']})
            source_and_target_alias.append(temp_list)
                
    return source_and_target_alias

#Send comparison reults mail
def send_comparison_result_mail(result_data_frame):
    
    with pd.ExcelWriter(f'{system_working_directory}/ACL_comparison_output.xlsx') as writer:  
        result_data_frame.to_excel(writer, sheet_name = "ACL Comparison Results", index=False)
    
    email_config_path = system_working_directory + '/_webMethods-Upgrade/config_files/email_config.yaml'
    pipeline_type = 'ACL Comparision'
    with open(email_config_path,'r') as f:
        email_config = yaml.safe_load(f)
    receipents = ['madhubabu.tammu@vodafone.com']
    #receipents = []
    #for i in email_config[pipeline_type]:  #flattening lists
    #    receipents.extend(i)
    cc = ['madhubabu.tammu@vodafone.com']
    # cc = []
    # for i in email_config['Cc']:  #flattening lists
    #     cc.extend(i)

    to = receipents
    from_mail = email_config['From']
    server = email_config['mailhost']
    
    body = f'''<p>Hi Team,<br><br>    PFA ACL Comparison Report for  source environment: <b style = "color: green;">{source_environment.upper()}</b>, target environment: <b style = "color: green;">{target_environment.upper()}</b>, zone: <b style = "color: green;">{zone}</b> and instance: <b style = "color: green;">{instance}</b>.<br><br> Regards,<br> WM-Upgrade-Team</p>'''
    body_part = MIMEText(body, 'html')
    msg = MIMEMultipart()
    msg.attach(body_part)
    
    #setting msg headers
    msg['From'] = from_mail
    msg['To'] = ','.join(to)
    msg['Cc'] = ','.join(cc)
    msg['Subject'] = f'ACL COMPARISON REPORT'
    to.extend(cc)

    part = MIMEBase('application', "octet-stream")

    send_file_path = f'{system_working_directory}/ACL_comparison_output.xlsx'
    if os.path.isfile(send_file_path):
        part.set_payload(open(send_file_path, "rb").read())
        encoders.encode_base64(part)
        file_name = f'ACLComparisonReport.xlsx'
        part.add_header('Content-Disposition',f'attachment; filename={file_name}')
        msg.attach(part)

    with SMTP(server) as mailer:
        mailer.sendmail(from_mail, to, msg.as_string())
    
    print("Mail sent successfully...")

def acl_comaprison():
    
    try:
        #Checking validity of source and target environments
        return_code = check_environment(source_environment)
        if return_code != 0:
            print_error(f"Invalid source environment: {source_environment}")
            return
        return_code = check_environment(target_environment)
        if return_code != 0:
            print_error(f"Invalid target environment: {target_environment}")
            return
        print_success("Environemnts are valid.")
        
        #Decrypting host vars
        source_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{source_environment}/host_vars'
        target_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{target_environment}/host_vars'
        source_decrypt_obj = DecryptHostvars(system_working_directory, source_environment, secret_value, source_hostvars_file_path)
        target_decrypt_obj = DecryptHostvars(system_working_directory, target_environment, secret_value, target_hostvars_file_path)
        source_decrypt_obj.decrypt()
        target_decrypt_obj.decrypt()
        print_success("Source and Target environment host_vars are decrypted successfully.")
        
        #Fetchiong source and target alias
        source_and_target_alias_list = fetch_source_and_target_alias()
        print_success(f"Source and Target alias lsit is formed. {source_and_target_alias_list}")

        source_environment_list = []
        target_environment_list = []
        zone_list = []
        instance_list = []
        package_name_list = []
        source_packages_exist_list = []
        target_packages_exist_list = []
        source_packages_status_list = []
        target_packages_status_list = []
        source_system_acl_element = []
        target_system_acl_element = []
        source_acl_tagged = []
        target_acl_tagged = []
        acl_match_list = []

        
        for source_and_target_alias in source_and_target_alias_list:
            source_instance = list(source_and_target_alias[0].keys())[0]
            target_instance = list(source_and_target_alias[1].keys())[0]
            source_host = source_and_target_alias[0][source_instance]
            target_host = source_and_target_alias[1][target_instance]
            
            #Comparison Object Creation
            comparison_object = ACLComparison(source_environment, target_environment, source_instance, target_instance, source_host, target_host, system_working_directory)
            
            return_code = comparison_object.fetch_package_folders()
            comparison_object.unzip_package_folders()
            source_packages_list, no_manifest_packages_source = comparison_object.fetch_packages_list('source')
            target_packages_list, no_manifest_packages_target = comparison_object.fetch_packages_list('target')

            source_cnf_list = comparison_object.fetch_cnf_files('source')
            target_cnf_list = comparison_object.fetch_cnf_files('target')
            print(source_packages_list,'\n', target_packages_list,'\n', source_cnf_list, '\n', target_cnf_list)
            print(f"No.of packages in source: {len(source_packages_list)}, target: {len(target_packages_list)}")
            print(f"No.of cnf files in source: {len(source_cnf_list)}, target: {len(target_cnf_list)}")

            
            packages_list = source_packages_list[:]
            packages_list.sort()
            
            cnf_list = source_cnf_list[:]
            cnf_list.extend(target_cnf_list)
            
            
            for package_name in packages_list:                
                result = comparison_object.fetch_status(package_name, 'target')
                if result == 1:
                    target_packages_exist_list.append("No")
                    target_packages_status_list.append("NA")                   
                else:
                    target_packages_exist_list.append("Yes")
                    result_list = result.split(',')
                    target_packages_status_list.append(result_list[0])
            
                result = comparison_object.fetch_status(package_name, 'source')

                if result == 1:
                    source_packages_exist_list.append("No")
                    source_packages_status_list.append("NA")                  
                else:
                    source_packages_exist_list.append("Yes")
                    result_list = result.split(',')
                    source_packages_status_list.append(result_list[0])

                if source_packages_status_list[-1] == 'Enabled' and target_packages_status_list[-1] == 'Enabled':
                    source_acl_element_list, source_acl_value_list = comparison_object.fetch_acl_elements(package_name, cnf_list[0],'source')
                    target_acl_element_list, target_acl_value_list = comparison_object.fetch_acl_elements(package_name, cnf_list[1],'target')

                    ss = source_packages_status_list.pop()
                    se = source_packages_exist_list.pop()
                    ts = target_packages_status_list.pop()
                    te = target_packages_exist_list.pop()

                    if len(source_acl_element_list)==0 :    
                        source_environment_list.append(source_environment)
                        target_environment_list.append(target_environment)
                        zone_list.append(comparison_object.source_alias_list[1])
                        instance_list.append(comparison_object.source_alias_list[2])
                        package_name_list.append(package_name)
                        source_packages_status_list.append(ss)
                        source_packages_exist_list.append(se)
                        target_packages_status_list.append(ts)
                        target_packages_exist_list.append(te)
                        source_system_acl_element.append('No-ACLs-tagged')
                        target_system_acl_element.append('No-ACLs-tagged')
                        source_acl_tagged.append('No-ACLs-tagged')
                        target_acl_tagged.append('No-ACLs-tagged')
                        acl_match_list.append('ACL-Doesnt-exist')
                    else:
                        for i in range(len(source_acl_element_list)):
                            if source_acl_element_list[i] in target_acl_element_list:
                                index = target_acl_element_list.index(source_acl_element_list[i])
                                source_environment_list.append(source_environment)
                                target_environment_list.append(target_environment)
                                zone_list.append(comparison_object.source_alias_list[1])
                                instance_list.append(comparison_object.source_alias_list[2])
                                package_name_list.append(package_name)
                                source_packages_status_list.append(ss)
                                source_packages_exist_list.append(se)
                                target_packages_status_list.append(ts)
                                target_packages_exist_list.append(te)
                                source_system_acl_element.append(source_acl_element_list[i])
                                target_system_acl_element.append(target_acl_element_list[index])
                                source_acl_tagged.append(source_acl_value_list[i])
                                target_acl_tagged.append(target_acl_value_list[index])
                                if source_acl_tagged[-1]==target_acl_tagged[-1]:
                                    acl_match_list.append('ACL-matched')
                                else:
                                    acl_match_list.append('ACL-mis-matched')
                            else:
                                source_environment_list.append(source_environment)
                                target_environment_list.append(target_environment)
                                zone_list.append(comparison_object.source_alias_list[1])
                                instance_list.append(comparison_object.source_alias_list[2])
                                package_name_list.append(package_name)
                                source_packages_status_list.append(ss)
                                source_packages_exist_list.append(se)
                                target_packages_status_list.append(ts)
                                target_packages_exist_list.append(te)
                                source_system_acl_element.append(source_acl_element_list[i])
                                target_system_acl_element.append('No-ACLs-tagged')
                                source_acl_tagged.append(source_acl_value_list[i])
                                target_acl_tagged.append('No-ACLs-tagged')
                                acl_match_list.append('ACL-mis-matched')
                
                else:
                    ss = source_packages_status_list.pop()
                    se = source_packages_exist_list.pop()
                    ts = target_packages_status_list.pop()
                    te = target_packages_exist_list.pop()

                    source_environment_list.append(source_environment)
                    target_environment_list.append(target_environment)
                    zone_list.append(comparison_object.source_alias_list[1])
                    instance_list.append(comparison_object.source_alias_list[2])
                    package_name_list.append(package_name)
                    source_packages_status_list.append(ss)
                    source_packages_exist_list.append(se)
                    target_packages_status_list.append(ts)
                    target_packages_exist_list.append(te)  
                    source_system_acl_element.append('No-ACLs-tagged')
                    target_system_acl_element.append('No-ACLs-tagged')
                    source_acl_tagged.append('No-ACLs-tagged')
                    target_acl_tagged.append('No-ACLs-tagged')
                    acl_match_list.append('ACL-Doesnt-exist')

            packages_list = no_manifest_packages_source[:]
            packages_list.sort()

            for i in packages_list:
                result = comparison_object.fetch_status(package_name, 'target')
                if result == 1:
                    target_packages_exist_list.append("No")
                    target_packages_status_list.append("NA")                   
                else:
                    target_packages_exist_list.append("Yes")
                    result_list = result.split(',')
                    target_packages_status_list.append(result_list[0])
                               
                result = comparison_object.fetch_status(package_name, 'source')
                if result == 1:
                    source_packages_exist_list.append("No")
                    source_packages_status_list.append("NA")                   
                else:
                    source_packages_exist_list.append("Yes")
                    result_list = result.split(',')
                    source_packages_status_list.append(result_list[0])

                source_environment_list.append(source_environment)
                target_environment_list.append(target_environment)
                zone_list.append(comparison_object.source_alias_list[1])
                instance_list.append(comparison_object.source_alias_list[2])
                package_name_list.append(i)
                source_system_acl_element.append('No-ACLs-tagged')
                target_system_acl_element.append('No-ACLs-tagged')
                source_acl_tagged.append('No-ACLs-tagged')
                target_acl_tagged.append('No-ACLs-tagged')
                acl_match_list.append('ACL-Doesnt-exist')

            comparison_object.remove_buffer_directories()
                    
        result_data_frame = pd.DataFrame({'Source Environment': source_environment_list, 'Target Environment': target_environment_list, 'Zone': zone_list, 'Instance': instance_list, 'Package name': package_name_list, 'Source-system-ACL-Element': source_system_acl_element, 'Target-system-ACL-Element': target_system_acl_element, 'Source-ACL-tagged': source_acl_tagged, 'Target-ACL-tagged': target_acl_tagged, 'ACL_match_list': acl_match_list}, dtype = str)    
        # 'Package Exists - Source': source_packages_exist_list, 'Package Exists - Target': target_packages_exist_list,'Source package status list': source_packages_status_list, 'Target package status list': target_packages_status_list,
        send_comparison_result_mail(result_data_frame)
    except Exception as e:
        traceback.print_exc()
        print_error(e)
    
acl_comaprison()