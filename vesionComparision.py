#importing required modules
import os, xmltodict

#Initialization of empty list
package_list = []
version_list = []

#function for getting package names as a list
def get_package_names(str):
  for path, dirnames, filenames in os.walk(str):
      for file_name in filenames:
          file_name = os.path.join(path, file_name)
          if file_name.endswith(".v3"):
            package_list.append(file_name)
  return package_list

#function for getting version names as a list
def get_version(package_list):
  for each_file_location in package_list:
      with open(each_file_location, 'r') as file:
          my_xml = file.read()
      my_dict = xmltodict.parse(my_xml)
      version = my_dict['Values']['value'][2]['#text']
      version_list.append(version)
  return version_list

#function calls
package_list = get_package_names('wm1/packages')
get_version(package_list)

#printing packages and version names
print('packages:', package_list, '\npackage versions:', version_list)