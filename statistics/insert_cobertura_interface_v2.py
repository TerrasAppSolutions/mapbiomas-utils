import insert_cobertura_postgres
import insert_cobertura_municipios_postgres
import argparse
from functools import reduce
import json

def get_info_project(project_name):
    if project_name == 'chaco':
       data = json.load(open('info_chaco.json')) 
    else:
        raise Exception('this project name doesnt exist')
    return data

def send_to_postgres_municipios(path_json, idprefix = 0):
    data = insert_cobertura_municipios_postgres.get_data(path_json)

    data_municipios = insert_cobertura_municipios_postgres.get_data_municipios(data)
    data_estados = insert_cobertura_municipios_postgres.get_data_estados(data)
    data_pais = insert_cobertura_municipios_postgres.get_data_pais(data)

    data_municipios_formatted = insert_cobertura_municipios_postgres.format_data(data_municipios, 'featureid', idprefix)
    data_estados_formatted = insert_cobertura_municipios_postgres.format_data(data_estados, 'UF', idprefix)
    data_pais_formatted = insert_cobertura_municipios_postgres.format_data(data_pais, 'PAIS', idprefix)

    insert_cobertura_municipios_postgres.insert_postgres(data_municipios_formatted)
    insert_cobertura_municipios_postgres.insert_postgres(data_pais_formatted)
    insert_cobertura_municipios_postgres.insert_postgres(data_estados_formatted)

def get_path_json(path_folder, year, filter_layer):

    print((filter_layer, year))
    json_path = insert_cobertura_postgres.get_cobertura_meta(path_folder,
    filter_layer, str(year))[0]['json_path']
    return json_path

def send_to_postgres(path_json, idprefix = 0):
    
    data = insert_cobertura_postgres.get_data(path_json)
    data_formatted = insert_cobertura_postgres.format_data(data, idprefix)
    insert_cobertura_postgres.insert_postgres(data_formatted)

def send_single_layer(layer, idprefix, path_folder, years):
    for year in years:
        path_json = get_path_json(path_folder, year, layer)
        send_to_postgres(path_json, idprefix)

def start_all_layers(info_project, dir_geojson):
    for info_layer in info_project['layers']:
        layer = info_layer['layer']
        start_one_layer(info_project, dir_geojson, layer)

def start_one_layer(info_project, dir_geojson, layer):
    info_layer = [_ for _ in info_project['layers'] if _['layer'] == layer][0]
    idprefix = info_layer['prefix']
    years = info_project['years']
    send_single_layer(layer, idprefix, dir_geojson, years)

def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')

    parser.add_argument('project', type=str, help='write the project name', choices=['brasil', 'chaco', 'raisg'])

    parser.add_argument('layer', type=str, help='write the layer name')

    parser.add_argument('dir_geojson', type=str,  help='write the geojson folder path')
    
    
    project = parser.parse_args().project
    layer = parser.parse_args().layer
    dir_geojson = parser.parse_args().dir_geojson

    info_project = get_info_project(project)

    if layer == 'all':
        start_all_layers(info_project, dir_geojson)
    else:
        start_one_layer(info_project, dir_geojson, layer)


    

if __name__ == "__main__":
    interface()    


    
