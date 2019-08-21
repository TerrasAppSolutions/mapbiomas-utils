
from info_lib import get_info_project
from export_gcs_server import export_geojson_GCS_to_server
import  insert_cobertura_interface
import insert_transition_interface

def export_server(info):
    gcs_url = info["statistics"]["gs_bucket"]["all"]
    dir_dst = info["statistics"]["folder"]["all_dev"]
    export_geojson_GCS_to_server(gcs_url, dir_dst)

def insert_cobertura(info):
    dir_geojson = info["statistics"]["folder"]["all_dev"]
    insert_cobertura_interface.start_all_layers(info, dir_geojson)

def insert_transicao(info):
    dir_geojson = info["statistics"]["folder"]["all_dev"]
    insert_transition_interface.start_all_layers(info, dir_geojson)

def start(col, project='brasil'):
    info = get_info_project(project) 
    info = [item for item in info if item['col'] == col][0]
    # export_server(info)
    # insert_cobertura(info)
    insert_transicao(info)
    

if __name__ == "__main__":
    start('4')