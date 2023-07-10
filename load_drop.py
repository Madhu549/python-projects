import yaml
import json
from pprint import pprint

file_path = "other_config.yml"
with open(file_path) as f:
    build_config = yaml.load(f, Loader=yaml.FullLoader)
pprint(build_config['otherConfigDB']['R2306'][6])                                     