import config
import os




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