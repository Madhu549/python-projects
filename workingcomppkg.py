from distutils.version import Version
import warnings
warnings.filterwarnings("ignore")
import sys
import shlex
import zipfile
import os
import traceback
import filecmp
import subprocess
import pandas as pd
import yaml
import xmltodict
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Importing utils
sys.path.insert(1, f'{sys.argv[1]}/_webMethods-Upgrade/python/utils')
from decrypt_hostvars import DecryptHostvars
from error_handling import ExecutionFlowError

#System arguments assignment
server_alias = sys.argv[2]
system_working_directory = sys.argv[1]
environment = sys.argv[3]
secret_value = sys.argv[4] 

class PackageComparison:
    
    #Constructor
    def __init__(self, server_alias, data_center,system_working_directory, environment, zone, instance, check_cluster):
        self.server_alias = server_alias
        self.data_center = data_center
        self.system_working_directory = system_working_directory
        self.environment = environment
        self.inventory = f"{system_working_directory}/_webMethods-Upgrade/config_files/wm_migration/{environment}/hosts"
        self.check_cluster = check_cluster
        self.zone = zone
        self.instance = instance
        
        #Forming extracting folder names
        self.extracted_packages_old = f"{self.system_working_directory}/extracted_packages_old"
        self.extracted_packages_new = f"{self.system_working_directory}/extracted_packages_new"
        
        #Forming zone and data center string based on cluster check variable
        if check_cluster:
            self.zone_and_data_center = f"{self.zone}_{self.data_center}"
        else:
            self.zone_and_data_center = self.zone
                
        #Forming packages zip file names
        self.old_packages_path = f"{environment}_{self.zone}_{self.instance}_old"
        self.new_packages_path = f"{environment}_{self.zone}_{self.instance}_new"
        
        print("Comparison object Successfully Initialized...")
        
        
    #Fecthing package folders from old and new servers 
    def fecth_package_folders(self):
        
        play_path = f"{self.system_working_directory}/_webMethods-Upgrade/playbooks/package_comparison/archive_to_local.yaml"
        
        #Forming old and new hostnames
        if self.check_cluster:
            old_hostname = f"wm{self.environment}{self.zone}{self.data_center}_old"
            new_hostname = f"wm{self.environment}{self.zone}{self.data_center}_new"
        else:
            old_hostname = f"wm{self.environment}{self.zone}_old"
            new_hostname = f"wm{self.environment}{self.zone}_new"
        
        #Calling playbook
        play_command = f'ansible-playbook {play_path} -i {self.inventory} --limit {self.zone_and_data_center} --extra-vars "instance={self.instance} new_pkg_name={self.new_packages_path} old_pkg_name={self.old_packages_path} old_hostname={old_hostname} new_hostname={new_hostname} system_working_directory={self.system_working_directory}"'
        print(play_command)
        output = subprocess.run(shlex.split(play_command))
        print("Playbook Output: ", output)
        print("Fetching packages completed....")
     
    #Unzipping package folder function
    def unzip_package_folders(self):
        
        old_path = f"{self.system_working_directory}/buffer/{self.old_packages_path}.zip"
        new_path = f"{self.system_working_directory}/buffer/{self.new_packages_path}.zip"
        
        #Unzipping old packages folder
        with zipfile.ZipFile(old_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_old)
            
        #Unzipping new packages folder
        with zipfile.ZipFile(new_path, 'r') as zip_ref:
            zip_ref.extractall(self.extracted_packages_new)
            
        print("Unzipping package folders is successfully completed...")

    #Fecthing packages list from old packages folders
    def fecth_packages_list(self, type):
        
        print(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        packages_list = os.listdir(f"{self.system_working_directory}/extracted_packages_{type}/packages")
        
        temporary_list = packages_list[:]
        
        for package in temporary_list:
            if os.path.isdir(f"{self.system_working_directory}/extracted_packages_{type}/packages/{package}") == False:
                packages_list.remove(package)
            
        print(f"Successfully fetched packages names for type: {type}")
        
        return packages_list
    
    #Fetching Different files
    '''def print_diff_files(self, dcmp, cmp_result):
        if len(dcmp.left_only) > 0:
            cmp_result.append(f"{dcmp.left_only} are missing in {dcmp.right}\n")
        if len(dcmp.right_only) > 0:
            cmp_result.append(f"{dcmp.right_only} are missing in {dcmp.left}\n")
        for name in dcmp.diff_files:
            cmp_result.append("diff_file %s found in %s and %s\n" % (name, dcmp.left,
                dcmp.right))
        for sub_dcmp in dcmp.subdirs.values():
            self.print_diff_files(sub_dcmp, cmp_result)'''
                   
    #performing package comparison
    '''def perform_package_compaison(self, package_name):
        
        #Forming package paths for old and new IS
        old_package_path = f"{self.extracted_packages_old}/packages/{package_name}"
        new_package_path = f"{self.extracted_packages_new}/packages/{package_name}"
        
        #Checking the package folder in new IS or not
        if os.path.exists(new_package_path):

            cmp_result = []
            dcmp = filecmp.dircmp(old_package_path, new_package_path) 
            self.print_diff_files(dcmp, cmp_result)
            if len(cmp_result) == 0:
                result = 'Identical'
            else:
                result = ''.join(cmp_result)
            
            return result

        else:
            return f"{package_name} is not present in new IS."'''
    
    def return_value_status(self, values):
        try:
            value = values['#text']
            if value == 'yes':
                return 'Enabled'
            else:
                return 'Disabled'
        except KeyError:
            return 'NA'

    def return_value_version(self, values):
        try:
            value = values['#text']
            return value
        except KeyError:
            return 'NA'


    #Method to fetch the package_version and package_status
    def fetch_version_status(self, package_name, type):
        
        if type == 'new':
            extracted_path = self.extracted_packages_new
        else:
            extracted_path = self.extracted_packages_old
        
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
                    status = self.return_value_status(values)
                    
                elif values['@name'] == 'version':
                    version_flag = False
                    version = self.return_value_version(values)

            if version_flag:
                version = 'NA'
            if enabled_flag:
                status = 'NA'    
                
            return f"{status},{version}"

        else:
            return 1
    
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
    # decrypting hostvars files
    hostvars_file_path = f'{system_working_directory}/_webMethods-Upgrade/config_files/wm_migration/{environment}/host_vars'
    decrypt_obj = DecryptHostvars(system_working_directory, environment, secret_value, hostvars_file_path)
    decrypt_obj.decrypt()
    
    server_alias_list = server_alias.split('_')
    zone = server_alias_list[0]
    instance = server_alias_list[1]
    check_cluster = environment in ['cob1', 'cob2', 'cob3', 'tems1', 'tems2', 'tems3', 'tems4']
    #Checking current environment is cluster or not
    if check_cluster:
        if len(server_alias_list) != 3:
            raise Exception(f"Invalid server alias for cluster environment: {environment}")
        else:
            data_center = server_alias_list[2]
            print(f"Cluster Environment detected.. data center = {data_center}.")
    else:
        data_center = None
        print("Not Cluster Environment..")
        comparison_object = PackageComparison(server_alias, data_center, system_working_directory, environment, zone, instance, check_cluster)
        return_code = comparison_object.fecth_package_folders()
        comparison_object.unzip_package_folders()
        old_packages_list = comparison_object.fecth_packages_list('old')
        new_packages_list = comparison_object.fecth_packages_list('new')
        print(f"No.of packages old: {len(old_packages_list)}, new: {len(new_packages_list)}")

        #comparison_results = []
        package_names = []
        zones = []
        instances = []
        environment_list = []
        old_exists_list = []
        new_exists_list = []
        old_version_list = []
        old_status_list = []
        new_version_list = []
        new_status_list = []
        version_matched_list = []
        status_matched_list = []

        packages_list = old_packages_list[:]
        packages_list.extend(new_packages_list)
        packages_list = list(set(packages_list))
        
        for package_name in packages_list:
            package_names.append(package_name)
            zones.append(zone)
            instances.append(instance)
            environment_list.append(environment.upper())
            #comparison_result = comparison_object.perform_package_compaison(package_name)
            
            result = comparison_object.fetch_version_status(package_name, 'new')
            if result == 1:
                new_exists_list.append("No")
                new_status_list.append("NA")
                new_version_list.append("NA")
            else:
                new_exists_list.append("Yes")
                result_list = result.split(',')
                new_status_list.append(result_list[0])
                new_version_list.append(result_list[1])
                
            result = comparison_object.fetch_version_status(package_name, 'old')
            if result == 1:
                old_exists_list.append("No")
                old_status_list.append("NA")
                old_version_list.append("NA")
            else:
                old_exists_list.append("Yes")
                result_list = result.split(',')
                old_status_list.append(result_list[0])
                old_version_list.append(result_list[1])
                
            if (new_status_list[-1] == old_status_list[-1]):
                status_matched_list.append("Yes")
            else:
                status_matched_list.append("No")
            
            if (new_version_list[-1] == old_version_list[-1]):
                version_matched_list.append("Yes")
            else:
                version_matched_list.append("No")
        
        result_data_frame = pd.DataFrame({'Environment': environment_list, 'Zone': zones, 'Instance': instances, 'Package Name': package_names, 'Package Exists - Source': old_exists_list, 'Package Exists - Target': new_exists_list, 'Package Status - Source': old_status_list, 'Package Status - Target': new_status_list, 'Package Status - Match': status_matched_list, 'Package Version - Source': old_version_list, 'Package Version - Target': new_version_list, 'Package Version Match': version_matched_list}, dtype = str)
        
        comparison_object.send_comparison_result_mail(result_data_frame)
    
    
except Exception as error_message:
    traceback.print_exc()
    #Initializing error object using ExecutionFlowError
    error_obj = ExecutionFlowError(f"Error occured while comparing packages: {error_message}")