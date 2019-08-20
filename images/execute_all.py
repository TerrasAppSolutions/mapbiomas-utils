from  export_gcs_servidor import export_images_GCS_to_server
from info_lib import get_info_project

def create_folders_server(cobertura=True, transicao=True, RGB=True):
    """create the necessary folder in the server"""

def export_to_server(info):
    #cobertura
    gcs_url = info["gs_bucket"]["integracao"]
    dir_dst = info["folders"]["integracao"]
    export_images_GCS_to_server(gcs_url, dir_dst)
    #transicao
    gcs_url = info["gs_bucket"]["transicao"]
    dir_dst = info["folders"]["transicao"]
    export_images_GCS_to_server(gcs_url, dir_dst)




def start(col, project='brasil'):
    info = get_info_project(project) 
    info = [item for item in info if item['col'] == col][0]

    export_to_server(info)
    
if __name__ == "__main__":
    start('4')