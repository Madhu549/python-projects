import yaml
import traceback
import sys, os, pprint

#taking system arguments
file_path = 'C:\\Users\MADHU\Desktop\python\Python_Coding\\test10.yaml'

#and printing the traceback
#Print error messages
def print_error_and_exit(error_message):
    print(error_message)
    sys.stderr.write(error_message)
    sys.exit(0)

#Drop/Master/IS other yaml loading
def yaml_loader(path, error_message):
  if os.path.exists(path):
    try:
      with open(path, 'r') as file:
        data = yaml.load(file, Loader= yaml.FullLoader)
        pprint.pprint(data)
        return 'Yaml is in a proper format'
    except:
      traceback.print_exc()
      print_error_and_exit(error_message)
  else:
    print_error_and_exit(f'Invalid path: {path}')

#main function call
if __name__=='__main__':
  yaml_dict = yaml_loader(file_path, "Error in loading Yaml file............Please check the format")
  print(yaml_dict)