import  infra_lib

def insert_cobertura(path_geojson):

    data = infra_lib.get_data(path_geojson)

    data_municipios = infra_lib.get_data_municipios(data)
    data_estados = infra_lib.get_data_estados(data)
    data_pais = infra_lib.get_data_pais(data)

    
    data_municipios = infra_lib.format_data(data_municipios, col_territorio='featureid')
    data_estados = infra_lib.format_data(data_estados, col_territorio='UF')
    data_pais = infra_lib.format_data(data_pais, col_territorio='PAIS')


    infra_lib.insert_postgres(data_municipios)
    infra_lib.insert_postgres(data_estados)
    infra_lib.insert_postgres(data_pais)       


def start(project='brasil', col='4'):
    
    info = infra_lib.get_info_project(project)

    info = [item for item in info if item['col'] == col][0]
    
    paths_geojson = infra_lib.get_geojsons(info["statistics"]['folder']['all_dev']) 
    
    for path in paths_geojson:
        insert_cobertura(path)

    
if __name__ == "__main__":
    start()