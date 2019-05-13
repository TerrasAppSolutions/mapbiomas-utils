import os

def get_all_geojsons_paths(path_folder):
    geojsons_paths = []
    for root, dirs, files in os.walk(path_folder):
        geojsons_paths = geojsons_paths + [os.path.join(root,file) for file in files if file.endswith(".geojson")]
    geojsons_paths =  [path for path in geojsons_paths if 'transicao' in path]
    return geojsons_paths

transition_folder = "/home/dyeden/Documents/chaco/estatistica/COLECAO1"

paths = get_all_geojsons_paths(transition_folder)

for path in paths:
    endname_split = path.split("/")[-1].split('-')[4:]
    endname_original = '-'.join(endname_split)
    endname_new = endname_split[0] + '.' + endname_split[1] + '-1-ee_export.geojson'


    new_path = path.replace(endname_original, endname_new)

    print(path)
    print(new_path)

    os.system('mv ' + path + ' ' + new_path)
    # print(path)


