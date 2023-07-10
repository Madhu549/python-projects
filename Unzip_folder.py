from zipfile import ZipFile
from os import rename
import traceback
import os,acl
file_list = []

with ZipFile('C:\\Users\MADHU\Desktop\python_coodes\Python_Coding\CwB2BCPSPartnerServices.zip') as zf:
    for file_name in zf.namelist():
        for root, dir, file in os.walk(f'C:\\Users\MADHU\Desktop\python_coodes\Python_Coding\CwB2BCPSPartnerServices.zip\{file_name}'):
            try:
                print(file)
                #filtering by filetype
                if file.endswith('.xml'):
                    file = f'C:/Users/MADHU/Desktop/python_coodes/Python_Coding/CwB2BCPSPartnerServices.zip/{file}'
                    print(file)
                    new_file_name = file.replace('.xml', '.xsl')
                    rename(file, new_file_name)
                    file_list.append(new_file_name)
            except:
                # traceback.print_exc()
                continue
print(file_list)
#"C:\Users\MADHU\Desktop\python_coodes\Python_Coding\CwB2BCPSPartnerServices.zip\ns\CwB2BCPSPartnerServices\service\pub\v100\AddOrder\flow.xml"
acl.print_error_and_exit('hi')

