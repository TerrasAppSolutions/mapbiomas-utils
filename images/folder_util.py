import config
import os



def get_info_project(project_name):
    if project_name == 'chaco':
       data = json.load(open('info_chaco.json')) 
    if project_name == 'brasil':
       data = json.load(open('info_brasil.json')) 
    else:
        raise Exception('this project name doesnt exist')
    return data

def dir_cobertura():

    osCommand = "gsutil -m cp -r " + gcs_url + " " +  dir_dst

    os.system(osCommand)
    

    """
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/INTEGRACAO
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/RGB
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/TRANSICAO
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/VRT/INTEGRACAO
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/VRT/RGB
    mkdir -p /mnt/disks/data/data2/collections/COLECAO4/VRT/TRANSICAO
    """