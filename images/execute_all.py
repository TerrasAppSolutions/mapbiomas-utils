from export_gcs_servidor import export_images_GCS_to_server
from info_lib import get_info_project
import buildvrt_util
import buildovr_util


def create_folders_server(cobertura=True, transicao=True, RGB=True):
    """create the necessary folder in the server"""


def export_to_server_integracao(info):

    gcs_url = info["gs_bucket"]["integracao"]
    dir_dst = info["folders"]["integracao"]
    export_images_GCS_to_server(gcs_url, dir_dst)


def export_to_server_transicao(info):

    gcs_url = info["gs_bucket"]["transicao"]
    dir_dst = info["folders"]["transicao"]
    export_images_GCS_to_server(gcs_url, dir_dst)


def create_vrt_integracao(info):
    dir_src = info["folders"]["integracao"]
    dir_dst = info["folders"]["integracao_vrt"]
    buildvrt_util.vrt_integration(dir_src, dir_dst, info)


def create_vrt_transicao(info):
    dir_src = info["folders"]["transicao"]
    dir_dst = info["folders"]["transicao_vrt"]
    buildvrt_util.vrt_transition(dir_src, dir_dst, info)


# def create_vrt_ovr_integracao(info):
#     dir_src = info["folders"]["integracao"]
#     dir_dst = info["folders"]["integracao_vrt"]
#     buildvrt_util.vrt_integration(dir_src, dir_dst)

#     for part in range(1,5):
#         ovr_integracao(dir_dst, str(part), info)


def start(col, project='brasil'):
    info = get_info_project(project)
    info = [item for item in info if item['col'] == col][0]

#     export_to_server_integracao(info)
#     create_vrt_integracao(info)
    
#     export_to_server_transicao(info)
    create_vrt_transicao(info)


if __name__ == "__main__":
    start('4')
