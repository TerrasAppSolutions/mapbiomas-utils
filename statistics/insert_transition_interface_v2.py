import insert_transition_postgres
import insert_transition_municipios_postgres
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
    data = insert_transition_municipios_postgres.get_data(path_json)

    data_municipios_formatted = insert_transition_municipios_postgres.format_data(data, idprefix)
    data_estados_formatted = insert_transition_municipios_postgres.format_data_estados(data, idprefix)
    data_pais_formatted = insert_transition_municipios_postgres.format_data_pais(data, idprefix)

    insert_transition_municipios_postgres.insert_postgres(data_municipios_formatted)
    insert_transition_municipios_postgres.insert_postgres(data_estados_formatted)
    insert_transition_municipios_postgres.insert_postgres(data_pais_formatted)


def send_to_postgres(path_json, idprefix = 0):
    data = insert_transition_postgres.get_data(path_json)
    data_formatted = insert_transition_postgres.format_data(data, idprefix)
    insert_transition_postgres.insert_postgres(data_formatted)

def get_path_json(path_folder, years_pair, filter_layer):
    year1 = years_pair.split('_')[0]
    year2 = years_pair.split('_')[1]
    json_path = insert_transition_postgres.get_transitions_meta(path_folder,
    filter_layer, year1=year1, year2=year2)[0]['json_path']
    return json_path

def send_single_layer(layer, idprefix, path_folder, transition_years):
    for years in transition_years:
        path_json = get_path_json(path_folder, years, layer)
        send_to_postgres(path_json, idprefix)

def start_all_layers(info_project, dir_geojson):
    for info_layer in info_project['layers']:
        layer = info_layer['layer']
        start_one_layer(info_project, dir_geojson, layer)

def start_one_layer(info_project, dir_geojson, layer):

    info_layer = [_ for _ in info_project['layers'] if _['layer'] == layer][0]

    idprefix = info_layer['prefix']
    transition_years = info_project['transition_years']
    send_single_layer(layer, idprefix, dir_geojson, transition_years)

def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')

    parser.add_argument('project', type=str, help='write the layer name',  choices=['brasil', 'chaco', 'raisg'])

    parser.add_argument('layer', type=str, help='write the layer name')

    parser.add_argument('dir_geojson', type=str,  help='the geojson folder')

    project = parser.parse_args().project
    layer = parser.parse_args().layer
    dir_geojson = parser.parse_args().dir_geojson

    info_project = get_info_project(project)


    if layer == "all":
        start_all_layers(info_project, dir_geojson)
    else:
        start_one_layer(info_project, dir_geojson, layer)


if __name__ == "__main__":
    interface()