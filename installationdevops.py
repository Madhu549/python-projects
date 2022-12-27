#importing required modules
import subprocess
import os, sys, traceback

#Assigning system arguments
env = sys.argv[1]
data_center = sys.argv[2]
zone = sys.argv[3]
template_name = sys.argv[4]
envtype = sys.argv[5]

try:
    #Forming properties file name
    property_filename = f'{env}_{data_center}_{zone}.properties'
    print("Properties File Name: ", property_filename)

    #Forming command and directory to run
    cmd = f"./sagcc exec   templates composite apply {template_name} -i {property_filename} environment.type={envtype} -username Administrator -password w3bm3thods"
    directory = '/opt/SP/comcen/CommandCentral/client/bin'
    print("Command to run: ", cmd)
    #changing current working directory to dictionary which we want to run th shell script
    os.chdir(directory)

    #Running shell script using subprocess module
    out = os.system(cmd)
    if out == 0:
        print("Installation started....")
    else:
        sys.stderr.write("Error occured while running installtion script...\n")
except:
    traceback.print_exc()
    sys.stderr.write("Exception occured while running shell script...\n")