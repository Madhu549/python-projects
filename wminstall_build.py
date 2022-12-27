#importing required modules

import subprocess
import os

#taking users input 

env = input("please enter Environment: ")
data_center = input("please enter Datacenter: ")
zone = input("please enter Zone: ")
template_name = input("please enter templateName: ")
property_filename = f'{env}_{data_center}_{zone}'
envtype = input('please enter envtype: ')


#Forming command and directory to run

cmd = f"'./sagcc exec   templates composite apply {templateName} -i {property_fileName} environment.type={envtype}'"
directory = '/opt/SP/comcen/CommandCentral/client/bin'

#changing current working directory to dictionary which we want to run th shell script

os.chdir(directory)

#Running shell script using subprocess module

subprocess.run(cmd)