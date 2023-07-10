task_name_type = 'db_deployment'
result = f"{' '.join([task_name_type.split('_')[0].split('-')[0].upper(), task_name_type.split('_')[0].split('-')[1].title(), task_name_type.split('_')[1].title()]) if len(task_name_type.split('_')[0].split('-')) > 1 else ' '.join([task_name_type.split('_')[0].split('-')[0].upper(), (task_name_type.split('_')[1].title())])}"
print(result)