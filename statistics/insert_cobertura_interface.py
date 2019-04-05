import insert_cobertura_postgres
import insert_cobertura_municipios_postgres
import argparse
from functools import reduce

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

    json_path = insert_cobertura_postgres.get_cobertura_meta(path_folder,
    filter_layer, str(year))
    return json_path

def send_to_postgres(path_json, idprefix = 0):
    
    data = insert_cobertura_postgres.get_data(path_json)
    data_formatted = insert_cobertura_postgres.format_data(data, idprefix)
    insert_cobertura_postgres.insert_postgres(data_formatted)

def biomas(path_folder, years):

    filter_layer = 'biomas'

    for year in years:             
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres(path_json)

def car_biomas(path_folder, years):

    idprefix=10000000
    filter_layer = 'car.biomas'

    for year in years:        
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres(path_json, idprefix)

def bacias_nivel_1(path_folder, years):

    idprefix = 7000000
    filter_layer = 'bacias.nivel.1'

    for year in years:        
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres(path_json,  idprefix)

def bacias_nivel_2(path_folder, years):

    idprefix = 7100000
    filter_layer = 'bacias.nivel.2'

    for year in years:   
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres(path_json,  idprefix)

def municipios(path_folder, years):

    filter_layer = 'municipios'

    for year in years:
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres_municipios(path_json)


def car_municipios(path_folder, years):

    idprefix = 10000000
    filter_layer = 'car.municipios'

    for year in years:
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres_municipios(path_json, idprefix)


def terra_indigena(path_folder, years):
    
    idprefix = 6000000
    filter_layer = 'ti'

    for year in years:
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres_municipios(path_json, idprefix)

def unidade_de_conservacao(path_folder, years):
    
    idprefix = 6000000
    filter_layer = 'uc'

    for year in years:
        path_json = get_path_json(path_folder, year, filter_layer)
        send_to_postgres_municipios(path_json, idprefix)


def all_layers(path_folder, years):
    for year in years:
        print(year)

        path_json = get_path_json(path_folder, year, 'biomas')
        send_to_postgres(path_json)

        path_json = get_path_json(path_folder, year, 'bacias.nivel.1')
        send_to_postgres(path_json, idprefix=7000000)

        path_json = get_path_json(path_folder, year, 'bacias.nivel.2')
        send_to_postgres(path_json, idprefix=7100000)

        path_json = get_path_json(path_folder, year, 'municipios')
        send_to_postgres_municipios(path_json)

        path_json = get_path_json(path_folder, year, 'ti')
        send_to_postgres(path_json, idprefix=6000000)

        path_json = get_path_json(path_folder, year, 'uc')
        send_to_postgres(path_json, idprefix=6000000)

        path_json = get_path_json(path_folder, year, 'car.biomas')
        send_to_postgres(path_json, idprefix=10000000)

        path_json = get_path_json(path_folder, year, 'car.municipios')
        send_to_postgres(path_json, idprefix=10000000)


def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')

    parser.add_argument('layer', type=str, help='choose the layer', 
                        choices=['biomas', 'car_biomas', 'bacias_nivel_1', 'bacias_nivel_2', 
                        'municipios_estado_pais', 'car_municipios', 'all'])

    parser.add_argument('dir_geojson', type=str,  help='the geojson folder')
    
    
    layer = parser.parse_args().layer
    dir_geojson = parser.parse_args().dir_geojson

    years = range(1985, 2018)
    if layer == "biomas":
        biomas(dir_geojson, years)
    
    if layer == "car_biomas":
        car_biomas(dir_geojson, years)

    if layer == "bacias_nivel_1":
        bacias_nivel_1(dir_geojson, years)

    if layer == "bacias_nivel_2":
        bacias_nivel_2(dir_geojson, years)

    if layer == "municipios_estado_pais":
        municipios(dir_geojson, years)

    if layer == "car_municipios":
        car_municipios(dir_geojson, years)

    if layer == 'all':
        all_layers(dir_geojson, years)


if __name__ == "__main__":
    interface()

