import insert_cobertura_postgres
import insert_cobertura_municipios_postgres
import argparse
from functools import reduce

def send_to_postgres_municipios(path_json, year, idprefix = 0):
    print(year)

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


def send_to_postgres(path_json, year, idprefix = 0):
    print(year)

    data = insert_cobertura_postgres.get_data(path_json)
    data_formatted = insert_cobertura_postgres.format_data(data, idprefix)
    insert_cobertura_postgres.insert_postgres(data_formatted)

def biomas(path_folder, years):

    for year in years:     
        path_json = path_folder + "/collection-31-cobertura-biomas-" + str(year) + "-4ee_export.geojson"
        send_to_postgres(path_json, year)

def car_biomas(path_folder, years):

    idprefix=10000000

    for year in years:   
        path_json = path_folder + "/collection-31-cobertura-biomas-car-" + str(year) + "-4ee_export.geojson"
        send_to_postgres(path_json, year,  idprefix)

def bacias_nivel_1(path_folder, years):

    idprefix = 7000000

    for year in years:   
        path_json = path_folder + "/collection-31-cobertura-bacias-nivel-1-" + str(year) + "-4ee_export.geojson"
        send_to_postgres(path_json, year,  idprefix)

def bacias_nivel_2(path_folder, years):

    idprefix = 7100000

    for year in years:   
        path_json = path_folder + "/collection-31-cobertura-bacias-nivel-2-" + str(year) + "-4ee_export.geojson"
        send_to_postgres(path_json, year,  idprefix)

def municipios(path_folder, years):

    for year in years:
        path_json = path_folder + "/collection-31-cobertura-municipios-" + str(year) + "-4ee_export.geojson"
        send_to_postgres_municipios(path_json, year)


def car_municipios(path_folder, years):
    idprefix = 10000000

    for year in years:
        path_json = path_folder + "/collection-31-cobertura-municipios-car-" + str(year) + "-4ee_export.geojson"
        send_to_postgres_municipios(path_json, year, idprefix)

def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')

    parser.add_argument('layer', type=str, help='choose the layer', 
                    choices=['biomas', 'car_biomas', 'bacias_nivel_1', 'bacias_nivel_2', 'municipios_estado_pais', 'car_municipios'])

    parser.add_argument('dir_geojson', type=str,  help='the geojon folder')
    
    
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


if __name__ == "__main__":
    interface()

