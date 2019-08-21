
from export_gcs_server import export_geojson_GCS_to_server
def export_server(info):
    gcs_url = info["statistics"]["gs_bucket"]["all"]
    dir_dst = info["statistics"]["folder"]["all"]
    export_geojson_GCS_to_server(gcs_url, dir_dst)

def start(col, project='brasil'):
    info = get_info_project(project) 
    info = [item for item in info if item['col'] == col][0]
    export_server(info)

if __name__ == "__main__":
    start('4')