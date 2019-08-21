import json

def get_info_project(project_name):
    if project_name == 'chaco':
       data = json.load(open('info_chaco.json')) 
    if project_name == 'brasil':
       data = json.load(open('info_brasil.json')) 
    else:
        raise Exception('this project name doesnt exist')
    return data
