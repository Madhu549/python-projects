#importing required modules
import os, xmltodict

zone = input("enter zone")
instance = input("enter instance")


#Version finder class
class Version_Finder():
    #Initialization of empty list
    def __init__(self):
        self.res = {}
        self.file_names_lst = []
        self.version_lst = []

#function for getting package names as a keys of dictonary

    def get_package_names(self, str):
        for path, dirnames, filenames in os.walk(str):
            for file_name in filenames:
                file_name = os.path.join(path, file_name)
                if file_name.endswith(".v3"):
                    self.file_names_lst.append(file_name)
        return self.file_names_lst

#function for getting version names as a values for corresponding package names

    def get_status_and_version(self, package_names):
        for each_file_location in package_names:
            with open(each_file_location, 'r') as file:
                my_xml = file.read()
            my_dict = xmltodict.parse(my_xml)
            version = my_dict["Values"]["value"][2]["#text"]
            self.version_lst.append(version)
            self.res[each_file_location] = version
#return dict(res),package_names version_lst
        return self.res, package_names, self.version_lst


#function calls
class_obj = Version_Finder()

package_version_dictionary1, package_names1, version_names1 = class_obj.get_status_and_version(
    class_obj.get_package_names(input('please enter package directory1: ')))
print(package_version_dictionary1)

package_version_dictionary2, package_names2, version_names2 = class_obj.get_status_and_version(
    class_obj.get_package_names(input('please enter package directory2: ')))

print(package_version_dictionary2)
'''
if package_version_dictionary1==package_version_dictionary2:
        print("same")
        print(package_names1,package_names2)'''

