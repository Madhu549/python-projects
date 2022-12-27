#importing required modules
import os, xmltodict, pprint

#Initialization of empty list
res = {}

#function for getting package names as a keys of dictonary
def get_package_names(str):
  for path, dirnames, filenames in os.walk(str):
    for file_name in filenames:
      file_name = os.path.join(path, file_name)      
      if file_name.endswith(".v3"):  
        res[file_name] = None
  return res

#function for getting version names as a values for corresponding package names
def get_version(res):
  for each_file_location in res.keys():
    with open(each_file_location, 'r') as file:
      my_xml = file.read()
    my_dict = xmltodict.parse(my_xml)
    version = my_dict['Values']['value'][2]['#text']
    res[each_file_location] = version
  return res

#function calls
package_names = get_package_names(input('please enter package directory: '))
dictionary = get_version(package_names)

#printing dictionary 
pprint.pprint(dictionary, indent = 1)
