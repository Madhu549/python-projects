# Importing modules

from ast import Return, main

import sys

import shlex

import subprocess

import traceback

import os

from time import sleep



# initialization of class

class WMInstall:

# initializing constructor

    def __init__(self, sys_working_dir, env, data_center, zone):

        self.sys_working_dir = sys_working_dir

        self.env = env

        self.data_center = data_center

        self.zone = zone

        # framming variables

        self.log_file = f'{shared_dir}/WM_Upgrade/wm_install.log'

        self.property_filename = f'{env}_{data_center}_{zone}.properties'

        self.template_name = f'{env}_{data_center}_{zone}'

        self.playbook_path = f'{sys_working_dir}/_webMethods-Upgrade/playbooks/wm_install.yaml'

        self.inventory = f'{sys_working_dir}/_webMethods-Upgrade/config_files/Upgrade/hosts'



    # method to run playbook and return playbook return code

    def runPlaybook(self,play_command):

        result = subprocess.run(shlex.split(play_command))

        if result.returncode == 0:

            print(f'playbook executed succesfully with return code:{result.returncode}')

            return result.returncode

        else:

            raise Exception(f'Encountered error while executing playbookwith return code:{result.returncode}')



    # method to fetch job_id from logfile

    def fetch_job_id(self):

        job_id = 23

        data = ''

        with open(self.log_file, 'r') as f:

            data = f.readlines()

        print(data)

        #Todo: code to return job_id

        return job_id



    # method to install is or spm

    def install_product(self, envtype):

        play_command = f'ansible-playbook -i {self.inventory} --extra-vars "envtype={envtype}"'

        print(f'Installing the product {self.envtype} is started')

        self.runPlaybook(play_command)

        # Todo: fetch the job id and return

        job_id = self.fetch_job_id()

        job_progress = self.fetch_job_progress(job_id)

        while job_progress != 'SUCCESS':

            sleep(30)

            return f'''Status of {job_id}  is:{job_progress}......

                       Next update on job progress will be given in next 30 seconds......'''

            

        else:

            print(f'Installation completed successfully for {envtype}.......')



    # method to return job progress

    def fetch_job_progress(self, job_id):

        play_path = f'{sys_working_dir}/_webMethods-Upgrade/playbooks/install_job_progress.yaml'

        play_command = f'ansible-playbook -i {self.inventory} --extra-vars "job_id={job_id}"'

        return self.runPlaybook(play_command)





# taking the system arguments

sys_working_dir = sys.argv[1]

env = sys.argv[2]

data_center = sys.argv[2]

zone = sys.argv[3]

shared_dir = sys.argv[4]



if __name__ == "__main__":

    # object creation

    try:

        obj = WMInstall(sys_working_dir, env, data_center, zone, shared_dir)

        # installing the SPM

        obj.install_product('gen_spm')

        # installing the IS

        obj.install_product('gen_is')

    # exception handling 

    except:

        traceback.print_exc("Exception")