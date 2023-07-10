import yaml

zone_and_instance_path = 'tree.yaml'

with open(zone_and_instance_path) as f:
    zone_and_instance = yaml.safe_load(f)

zones_list = list(zone_and_instance.keys()) 

def fetch_zone_and_instance_list(zone, instance): 
    server_alias_list = []
    if zone.upper() != 'ALL':
        if instance.upper() != 'ALL':
            server_alias_list.append(f"{zone_and_instance[zone]['alias']}_{instance}")
        else:
            for each_instance in zone_and_instance[zone]['instances']:
                server_alias_list.append(f"{zone_and_instance[zone]['alias']}_{each_instance}")
    else:
        if instance.upper() == 'ALL':
            for each_zone in zone_and_instance.keys():
                for each_instance in zone_and_instance[each_zone]['instances']:
                    server_alias_list.append(f"{zone_and_instance[each_zone]['alias']}_{each_instance}")
        else:
            for each_zone in zone_and_instance.keys():
                server_alias_list.append(f"{zone_and_instance[each_zone]['alias']}_{instance}")


    return server_alias_list

#print(zones_list)
print(fetch_zone_and_instance_list('edge', 'all'))