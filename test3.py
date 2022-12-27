import pickle
# dict = {1:'madhu', 2:'bababu'}

# with open('C:\\Users\MADHU\Desktop\\master_config.yaml', 'wb') as f:
#   xml_data = pickle.dump(dict, f)

with open('C:\\Users\MADHU\Desktop\\master_config.yaml', 'rb') as f:
  data = pickle.load(f)

print(data)