import getpass

env = getpass.getpass("please enter Environment: ")
data_center = getpass.getpass("please enter Datacenter: ")
zone = getpass.getpass("please enter Zone: ")
template_name = getpass.getpass("please enter templateName: ")
property_filename = f'{env}_{data_center}_{zone}'
envtype = getpass.getpass('please enter envtype: ')
print(property_filename)