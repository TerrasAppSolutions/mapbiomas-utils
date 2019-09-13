import  infra_lib

def insert_cobertura(path_geojson):

    data = infra_lib.get_data(path_geojson)

    data_municipios = infra_lib.get_data_municipios(data)
    data_estados = infra_lib.get_data_estados(data)
    data_pais = infra_lib.get_data_pais(data)

    
    data_municipios = infra_lib.format_data(data_municipios, col_territorio='featureid')
    data_estados = infra_lib.format_data(data_estados, col_territorio='UF')
    data_pais = infra_lib.format_data(data_pais, col_territorio='PAIS')


    infra_lib.insert_postgres_stats(data_municipios)
    infra_lib.insert_postgres_stats(data_estados)
    infra_lib.insert_postgres_stats(data_pais)       


def start(project='brasil', col='4'):
    
    info = infra_lib.get_info_project(project)

    info = [item for item in info if item['col'] == col][0]
    
    paths_geojson = infra_lib.get_geojsons(info["statistics"]['folder']['all']) 

    [path for path in paths_geojson if 'infra-5053-' in path]
    [path for path in paths_geojson if 'infra-10053-' in path]
    [path for path in paths_geojson if 'infra-20053-' in path]
    
    for path in paths_geojson:
        print(path)
        try:
            insert_cobertura(path)
        except Exception as e:
            print(str(e))


    
if __name__ == "__main__":
    start()


    gs://mapbiomas-dev-storage/ESTATISTICA_GEE/COLECAO4/INFRA/COBERTURAV2/collection-4.0-cobertura-infra-10006-1985-2-.geojson