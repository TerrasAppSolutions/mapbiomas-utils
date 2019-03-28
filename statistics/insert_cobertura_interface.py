import insert_cobertura_postgres
import argparse
from functools import reduce

def biomas(path_folder, years):

    for year in years:        

        path_json = path_folder + "/collection-31-cobertura-biomas-" + str(year) + "-4ee_export.geojson"

        data = insert_cobertura_postgres.get_data(path_json)

        data_formatted = insert_cobertura_postgres.format_data(data)

        insert_cobertura_postgres.insert_postgres(data_formatted)

def car_biomas(path_folder, years):

    idprefix=10000000

    for year in years:   
        path_json = path_folder + "/collection-31-cobertura-biomas-car-" + str(year) + "-4ee_export.geojson"

        data = insert_cobertura_postgres.get_data(path_json)

        data_formatted = insert_cobertura_postgres.format_data(data, idprefix)

        insert_cobertura_postgres.insert_postgres(data_formatted)

        print(year)

def interface():

    parser = argparse.ArgumentParser(description='Export the statistics for the postgres database')

    parser.add_argument('layer', type=str, help='choose the layer', 
                    choices=['biomas'])

    parser.add_argument('dir_geojson', type=str,  help='the geojon folder')
    
    
    layer = parser.parse_args().layer
    dir_geojson = parser.parse_args().dir_geojson

    years = range(1985, 2018)
    if layer == "biomas":
        biomas(dir_geojson, years)


if __name__ == "__main__":
    interface()

