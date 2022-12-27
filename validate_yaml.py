import yaml
import traceback
import sys, os

#taking system arguments
file_path = input("please enter path: ")

#and printing the traceback
#Print error messages
def print_error_and_exit(error_message):
    print(error_message)
    sys.stderr.write(error_message)
    sys.exit(0)

#Drop/Master/IS other yaml loading
def yaml_loader(path, error_message):
  try:
    if os.path.exists(path):
      with open(path, 'r') as file:
        yaml.load(file, Loader= yaml.FullLoader)
        return 'Yaml was is proper format'
    else:
        print(f'Invalid path: {path}')
        return
  except:
    traceback.print_exc()
    print_error_and_exit(error_message)

if __name__=='__main__':
  yaml_dict = yaml_loader(file_path, 'Error in loading Yaml file............Please check the format')
  print(yaml_dict)
  #"C:\\Users\MADHU\Desktop\master_config.yaml"