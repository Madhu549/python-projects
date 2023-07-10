import yaml

# Load YAML file
with open("C:\\Users\MADHU\Desktop\python\Python_Coding\drop.yaml", "r") as f:
    try:
        data = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        print(e)

# Define schema
schema = yaml.safe_load("""
type: object
properties:
  name:
    type: string
  age:
    type: integer
required:
  - name
""")

# Validate YAML file
try:
    yaml.validate(data, schema)
except yaml.ValidationError as e:
    print(e)

# Update YAML file
with open("file.yaml", "w") as f:
    yaml.dump(data, f)