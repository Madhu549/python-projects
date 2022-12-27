import subprocess
import os

#taking users input 
templateName = input("please enter templateName: ")
propertyFileName = input('please enter propertyFileName: ')
envtype = input('please enter envtype: ')

#Farming command and directory to run
cmd = f"'./sagcc exec   templates composite apply {templateName} -i {propertyFileName} environment.type={envtype}'"
directory = '/opt/SP/comcen/CommandCentral/client/bin'

#changing current working directory to dictionary which we want to run th shell script
os.chdir(directory)


#either os or subprocess module can be used to run shell script
#Running shell script using subprocess module
subprocess.run(cmd)

#running shell script using os module
os.system(cmd)