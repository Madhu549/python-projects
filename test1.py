#importing modules 
import sys
import shlex
import zipfile
import os
import traceback
import subprocess
import pandas as pd
import yaml
import xmltodict
import yaml
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Importing utils
sys.path.insert(1, f'{sys.argv[1]}/_webMethods-Upgrade/python/utils')
from decrypt_hostvars import DecryptHostvars
from error_handling import ExecutionFlowError


#taking system arguments input
source_environment = sys.argv[1]
target_environment = sys.argv[2]
zone = sys.argv[3]
instance = sys.argv[4]
system_working_directory = sys.argv[5]
data_center = sys.argv[6]
secret_value = sys.argv[7]



class PackageComparison:
    
    def form_server_host(self, server_list):
        
        if len(server_list) > 3:
            return f"wm{server_list[0]}{server_list[1]}{server_list[2]}{server_list[3]}"
        else:
            return f"wm{server_list[0]}{server_list[1]}{server_list[2]}"
    
    #Constructor
    def __init__(self, source_server_alias_list, target_server_alias_list, system_working_directory):
        
        self.source_server_alias_list = source_server_alias_list
        self.target_server_alias_list = target_server_alias_list
        self.system_working_directory = system_working_directory
        self.source_inventory = f"{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{source_environment}/hosts"
        self.target_inventory = f"{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{target_environment}/hosts"
        
        #Forming extracting folder names
        self.extracted_packages_source = f"{self.system_working_directory}/extracted_packages_source"
        self.extracted_packages_target = f"{self.system_working_directory}/extracted_packages_target"
        
        self.source_server_host = self.form_server_host(self.source_server_alias_list)
        self.target_server_host = self.form_server_host(self.target_server_alias_list)
        
        #Forming packages zip file names
        self.source_packages_path = f"{self.source_server_host}"
        self.target_packages_path = f"{self.target_server_host}"
        
        print("Comparison object Successfully Initialized...")

    #Fecthing package folders from source and target servers 
    def fecth_package_folders(self):
        
        play_path = f"{self.system_working_directory}/_webMethods-Upgrade/playbooks/package_comparison/archive_to_local.yaml"
        
        #Calling playbook
        play_command = f'ansible-playbook {play_path} -i {self.inventory} --limit {self.zone_and_data_center} --extra-vars "system_working_directory={self.system_working_directory}"'
        print(play_command)
        output = subprocess.run(shlex.split(play_command))
        print("Playbook Output: ", output)
        print("Fetching packages completed....")

    #Unzipping package folder function
    def unzip_package_folders(self):
        
        source_path = f"{self.system_working_directory}/buffer/{self.source_packages_path}.zip"
        target_path = f"{self.system_working_directory}/buffer/{self.target_packages_path}.zip"
        
        #Unzipping source packages folder
        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_source)
            
        #Unzipping target packages folder
        with zipfile.ZipFile(target_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_target)
            
        print("Unzipping package folders is successfully completed...")

    #Fecthing packages list from source packages folders
    def fecth_packages_list(self, type):
        
        print(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        packages_list = os.listdir(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        temporary_list = packages_list[:]
        
        for package in temporary_list:
            if os.path.isdir(f"{self.system_working_directory}/extracted_packages_{type}/packages/{package}") == False:
                packages_list.remove(package)
            
        print(f"Successfully fetched packages names for type: {type}")
        
        return packages_list

    #method for returning value
    def return_value(self, values):
        try:
            value = values['#text']
            return value
        except KeyError:
            return 'NA'


    #Method to fetch the package_version and package_status
    def fetch_version_status(self, package_name, type):
        
        if type == 'target':
            extracted_path = self.extracted_packages_target
        else:
            extracted_path = self.extracted_packages_source
        
        package_path = f"{extracted_path}/packages/{package_name}"
        
        if os.path.exists(package_path):
            with open(f'{package_path}/manifest.v3', 'r') as f:
                xml_data = f.read()

            xml_dict = xmltodict.parse(xml_data)

            enabled_flag = True
            version_flag = True

            for values in xml_dict['Values']['value']:
                if values['@name'] == 'enabled':
                    enabled_flag = False
                    status = self.return_value(values)
                    
                elif values['@name'] == 'version':
                    version_flag = False
                    version = self.return_value(values)

            if version_flag:
                version = 'NA'
            if enabled_flag:
                status = 'NA'    
                
            return f"{status},{version}"

        else:
            return 1
  



#function to fetch zone and instance from yaml file located in respective source and target directories
def fetch_zone_and_instance_list(environment, zone, instance, zone_and_instance_path, data_center = ''): 
    server_alias_list = []
    with open(zone_and_instance_path) as f:
        zone_and_instance = yaml.safe_load(f)
    if zone.upper() != 'ALL':
        if instance.upper() != 'ALL':
            if data_center == '':
                server_alias_list.append(f"{environment}_{zone}_{instance}")
            else:
                server_alias_list.append(f"{environment}_{zone}_{data_center}_{instance}")
        else:
            for each_instance in zone_and_instance[zone]['instances']:
                if data_center == '':
                    server_alias_list.append(f"{environment}_{zone}_{each_instance}")
                else:
                    server_alias_list.append(f"{environment}_{zone}_{data_center}_{each_instance}")
    else:
        if instance.upper() == 'ALL':
            for each_zone in zone_and_instance.keys():
                for each_instance in zone_and_instance[each_zone]['instances']:
                    if data_center == '':
                        server_alias_list.append(f"{environment}_{each_zone}_{each_instance}")
                    else:
                        server_alias_list.append(f"{environment}_{each_zone}_{data_center}_{each_instance}")
        else:
            for each_zone in zone_and_instance.keys():
                if data_center == '':
                    server_alias_list.append(f"{environment}_{each_zone}_{instance}")
                else:
                    server_alias_list.append(f"{environment}_{each_zone}_{data_center}_{instance}")

    return server_alias_list


source_zone_and_instance_path = 'dev.yaml'
target_zone_and_instance_path = 'sit3.yaml'


source_alias_list = fetch_zone_and_instance_list(source_environment, zone, instance, source_zone_and_instance_path, data_center)
target_alias_list = fetch_zone_and_instance_list(target_environment, zone, instance, source_zone_and_instance_path, data_center)

print(source_alias_list)
print('\n\n\n\n\n\n\n')
print(target_alias_list)




#function for spliting the server alias
def split_server_alias(server_alias):

    server_alias_list = server_alias.split('_')
    check_cluster = server_alias_list[0] in ['cob1', 'cob2', 'cob3', 'tems1', 'tems2', 'tems3', 'tems4']
    return check_cluster, server_alias_list



#function to send a mail
#Send comparison reults mail
def send_comparison_result_mail(self, result_data_frame):
    
    with pd.ExcelWriter(f'{system_working_directory}/package_comparison_output.xlsx') as writer:  
        result_data_frame.to_excel(writer, sheet_name = "Comparison Results", index=False)
    
    email_config_path = self.system_working_directory + '/_webMethods-Upgrade/config_files/email_config.yaml'
    pipeline_type = 'Package Comparison'
    with open(email_config_path,'r') as f:
        email_config = yaml.safe_load(f)
    receipents = []
    for i in email_config[pipeline_type]:  #flattening lists
        receipents.extend(i)
    cc = []
    for i in email_config['Cc']:  #flattening lists
        cc.extend(i)

    to = receipents
    from_mail = email_config['From']
    server = email_config['mailhost']
    
    body = f'''<p>Hi Team,<br><br>    PFA Package Comparison Report for environment: <b style = "color: green;">{self.environment.upper()}</b> and server_alias: <b style = "color: green;">{self.server_alias}</b>.<br><br> Regards,<br> WM-Upgrade-Team</p>'''
    body_part = MIMEText(body, 'html')
    msg = MIMEMultipart()
    msg.attach(body_part)
    
    #setting msg headers
    msg['From'] = from_mail
    msg['To'] = ','.join(to)
    msg['Cc'] = ','.join(cc)
    msg['Subject'] = f'PACKAGE COMPARISON REPORT'
    to.extend(cc)

    part = MIMEBase('application', "octet-stream")

    send_file_path = f'{system_working_directory}/package_comparison_output.xlsx'
    if os.path.isfile(send_file_path):
        part.set_payload(open(send_file_path, "rb").read())
        encoders.encode_base64(part)
        file_name = f'PackageComparisonReport.xlsx'
        part.add_header('Content-Disposition',f'attachment; filename={file_name}')
        msg.attach(part)

    with SMTP(server) as mailer:
        mailer.sendmail(from_mail, to, msg.as_string())
    
    print("Mail sent successfully...")


    

try:

    #framing host_vars file paths
    if source_environment and target_environment in ['cob1', 'cob2', 'cob3', 'tems1', 'tems2', 'tems3', 'tems4']:
        source_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{source_environment}_{data_center}_10.1/host_vars'
        target_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{target_environment}_{data_center}_10.7/host_vars'
    else:
        source_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{source_environment}_10.1/host_vars'
        target_hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/Inventory/{target_environment}_10.7/host_vars'
    

    source_decrypt_obj = DecryptHostvars(system_working_directory, source_environment, secret_value, source_hostvars_file_path)
    target_decrypt_obj = DecryptHostvars(system_working_directory, target_environment, secret_value, target_hostvars_file_path)
    source_decrypt_obj.decrypt()
    target_decrypt_obj.decrypt()

    #Splitting Server alias
    source_server_alias_dict = {}
    target_server_alias_dict = {}
    

    for each_server_alias in source_alias_list:
        invalid_flag, source_server_alias = split_server_alias(each_server_alias)
        source_server_alias_dict[each_server_alias] = source_server_alias

    for each_server_alias in target_alias_list:
        invalid_flag, target_server_alias = split_server_alias(each_server_alias)
        target_server_alias_dict[each_server_alias] = target_server_alias
    

    comparison_object = PackageComparison(source_alias_list, target_alias_list, system_working_directory)
    return_code = comparison_object.fecth_package_folders()
    comparison_object.unzip_package_folders()
    source_packages_list = comparison_object.fecth_packages_list('source')
    target_packages_list = comparison_object.fecth_packages_list('target')
    print(f"No.of packages source: {len(source_packages_list)}, target: {len(target_packages_list)}")

    package_names = []
    source_environment = []
    target_environment = []
    source_instance_list = []
    target_instance_list = []
    source_exists_list = []
    target_exists_list = []
    source_version_list = []
    source_status_list = []
    target_version_list = []
    target_status_list = []
    version_matched_list = []
    status_matched_list = []

    packages_list = source_packages_list[:]
    packages_list.extend(target_packages_list)
    packages_list = list(set(packages_list))


    source_env = source_alias_list[0]
    target_env = target_alias_list[0]
    source_instance = '_'.join(source_alias_list[1:])
    target_instance = '_'. join(target_alias_list[1:])
    
    for package_name in packages_list:
        package_names.append(package_name)
        source_environment.append(source_env)
        target_environment.append(target_env)
        source_instance_list.append(source_instance)
        target_instance_list.append(target_instance)

        result = comparison_object.fetch_version_status(package_name, 'target')
        if result == 1:
            target_exists_list.append("No")
            target_status_list.append("NA")
            target_version_list.append("NA")
        else:
            target_exists_list.append("Yes")
            result_list = result.split(',')
            target_status_list.append(result_list[0])
            target_version_list.append(result_list[1])
            
        result = comparison_object.fetch_version_status(package_name, 'source')
        if result == 1:
            source_exists_list.append("No")
            source_status_list.append("NA")
            source_version_list.append("NA")
        else:
            source_exists_list.append("Yes")
            result_list = result.split(',')
            source_status_list.append(result_list[0])
            source_version_list.append(result_list[1])
            
        if (target_status_list[-1] == source_status_list[-1]):
            status_matched_list.append("Yes")
        else:
            status_matched_list.append("No")
        
        if (target_version_list[-1] == source_version_list[-1]):
            version_matched_list.append("Yes")
        else:
            version_matched_list.append("No")
    
    #writing data into excell file
    result_data_frame = pd.DataFrame({'Source Environment': source_environment, 'Target Environment': target_environment, 'Source Instance': source_instance_list, 'Target Instance': target_instance_list, 'Package Name': package_names, 'Package Exists - Source': source_exists_list, 'Package Exists - Target': target_exists_list, 'Package Status - Source': source_status_list, 'Package Status - Target': target_status_list, 'Package Status - Match': status_matched_list, 'Package Version - Source': source_version_list, 'Package Version - Target': target_version_list, 'Package Version Match': version_matched_list}, dtype = str)
    send_comparison_result_mail(result_data_frame)
except Exception as error_message:
    traceback.print_exc()
    #Initializing error object using ExecutionFlowError
    error_obj = ExecutionFlowError(f"Error occured while comparing packages: {error_message}")